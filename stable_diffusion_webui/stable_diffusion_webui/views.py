from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage 
from django.conf import settings

import threading
import os
import pandas as pd
import json
import torch
from itertools import combinations
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

from .models import Prompt, GenerateRequest
from .utils import medium_options, style_options, artist_options, resolution_options, light_options, \
    list_to_matrix, do_paginator, translate_chinese_to_english



def index(request):
    options_list = [
        {"name": "Medium", "input_id": "medium", "options": medium_options},
        {"name": "Style", "input_id": "style", "options": style_options},
        {"name": "Artist", "input_id": "artist", "options": artist_options},
        {"name": "Resolution", "input_id": "resolution", "options": resolution_options},
        {"name": "Lighting", "input_id": "lighting", "options": light_options},
    ]
    context = {
        "options_list": options_list,
        "model_ids": settings.MODEL_IDS,
    }
    return render(request, "index.html", context)


def get_generate_request(request):
    """Get generate request information

    Args:
        request (Request):  Get parameters: 
            1. req_id: generate request id

    Returns:
        JsonResponse: {
            "n": int,
            "data": [
                {"id": int, "text": str, "image": str, "create_at": str}
            ]
        }
    """
    req_id = request.GET.get("req_id")
    generate_request = GenerateRequest.objects.get(id=req_id)

    resp = {
        "n": generate_request.prompt_count,
        "data": [],
        "matrix": []
    }

    for p in generate_request.prompts():
        item = {
            "id": p.id,
            "text": p.text,
            "image": p.image,
            'url': p.media_url(),
            "create_at": p.create_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        resp['data'].append(item)

    resp['matrix'] = list_to_matrix(resp['data'], col=3)
    return JsonResponse(resp)


def generate_image(request):
    """Use stable diffusion to generate multiple images by combination different properties.

    Args:
        request (Request): body is json format, detail is 
            {
                "subject": str,
                "medium": [str],
                "style": [str],
                "artist": [str],
                "website": [str],
                "resolution": [str],
                "color": [str],
                "lighting": [str],
                "seed": int,
                "steps": int,
                "width": int,
                "height": int,
                "model_id": str,
                "guidance_scale": float,
            } 
    """
    body = json.loads(request.body)
    subject = body['subject']
    subject, _  = translate_chinese_to_english(subject)
    combs = generate_combinations(
        subject,
        body.get('medium', []),
        body.get('style', []),
        body.get('artist', []),
        body.get('website', []),
        body.get('resolution', []),
        body.get('color', []),
        body.get('lighting', []),
    )
    generate_request = GenerateRequest.objects.create(request_body=body, combinations=combs)

    threading.Timer(1, do_generate_image, args=(body, combs, generate_request)).start()
    resp = {
        "id": generate_request.id,
        "combs": combs
    }
    return JsonResponse(resp)


def do_generate_image(body, combs, generate_request):
    model_id = body.get("model_id", "runwayml/stable-diffusion-v1-5") or "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("mps")
    pipe.enable_attention_slicing()
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    generator = torch.Generator("mps").manual_seed(body.get("seed", 0))

    prompts = []
    store = FileSystemStorage()
    for comb in combs:
        comb = list(filter(lambda x: x, comb))
        text = ",".join(comb)
        image = pipe(
            text, 
            num_inference_steps=body.get('steps', 20), 
            generator=generator, 
            width=body.get('width', 512),
            height=body.get('height', 512),
            guidance_scale=body.get('guidance_scale', 7.5)
            ).images[0]
        file_name = str(generate_request.id) + "_" + "_".join(list(comb)) + ".png"
        file_name = store.get_valid_name(file_name)
        image.save(store.path(file_name))
        
        prompt = Prompt.objects.create(
            text = text,
            image = store.path(file_name),
            request = generate_request,
        )
        prompts.append(prompt)

    return prompts


def generate_combinations(subject, mediums=[], styles=[], artistes=[], websites=[], resolutions=[], colors=[], lightings=[]):
    visited = []
    queue = []

    candidate_list = [
        [subject],
        mediums,
        styles,
        artistes,
        websites,
        resolutions,
        colors,
        lightings,
    ]
    node = (
        subject,
        mediums[0] if mediums else "",
        styles[0] if styles else "",
        artistes[0] if artistes else "",
        websites[0] if websites else "",
        resolutions[0] if resolutions else "",
        colors[0] if colors else "",
        lightings[0] if lightings else "",
    )
    queue.append(node)

    while queue:
        current_node = queue.pop(0)
        visited.append(current_node)

        # expand
        has_next = False
        next_node = list(current_node).copy()
        for i in range(len(next_node)):
            if next_node[i] == "":
                continue

            if has_next is True:
                break

            candidate = candidate_list[i]
            for c in candidate:
                try_node = next_node.copy()
                try_node[i] = c
                if tuple(try_node) not in visited:
                    next_node = try_node
                    has_next = True
                    break

        if not has_next:
            #have discovery all
            break

        next_node = tuple(next_node)
        queue.append(next_node)

    return visited

            
def history(request, page=1):
    generate_requests = GenerateRequest.objects.order_by("-id")
    pager = do_paginator(generate_requests, page)

    return render(request, "history.html", {'pager': pager, 'prefix': '/history/'})

    



    
    



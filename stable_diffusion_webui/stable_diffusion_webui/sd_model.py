from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, DiffusionPipeline
import torch


class SDModel:

    def __init__(self) -> None:
        self.device = "mps"
        if torch.cuda.is_available():
            self.device = "cuda"
        elif torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"
        self.base_model_id = "stabilityai/stable-diffusion-xl-base-1.0"
        self.refine_model_id = "stabilityai/stable-diffusion-xl-refiner-1.0"
        self.base_model: DiffusionPipeline = None
        self.refine_model: DiffusionPipeline = None

    def initial_models(self):
        if not self.base_model:
            self.base_model = DiffusionPipeline.from_pretrained(
                self.base_model_id, 
                resume_download=True, 
                use_safetensors=True,
                torch_dtype=torch.float32, 
                variant="fp32")
            #self.base_model.unet = torch.compile(self.base_model.unet, mode="reduce-overhead", fullgraph=True)
            self.base_model.to(self.device)

        if not self.refine_model:
            self.refine_model = DiffusionPipeline.from_pretrained(
                self.refine_model_id,
                text_encoder_2=self.base_model.text_encoder_2,
                vae=self.base_model.vae,
                torch_dtype=torch.float32,
                use_safetensors=True,
                variant="fp32",
            )
            self.refine_model.to(self.device)


default_sd_model = SDModel()

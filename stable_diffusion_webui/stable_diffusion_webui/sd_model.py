from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch


class SDModel:

    def __init__(self) -> None:
        self.id_pipeline_map = {}
        self.device = "mps"
        if torch.cuda.is_available():
            self.device = "cuda"
        elif torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"

    def get_model(self, model_id: str) -> StableDiffusionPipeline:
        if model_id in self.id_pipeline_map:
            return self.id_pipeline_map[model_id]
        
        pipe = StableDiffusionPipeline.from_pretrained(model_id, resume_download=True)
        pipe = pipe.to("mps")
        pipe.enable_attention_slicing()
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        self.id_pipeline_map[model_id] = pipe

        return pipe


default_sd_model = SDModel()
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler


class SDModel:

    def __init__(self) -> None:
        self.id_pipeline_map = {}

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
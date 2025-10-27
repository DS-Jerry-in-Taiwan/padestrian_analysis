class PipelineController:
    def __init__(self, preprocessor, model_analyzer, postprocessor):
        self.preprocessor = preprocessor
        self.model_analyzer = model_analyzer
        self.postprocessor = postprocessor
        
    def run(self, input_data):
        # Preprocess input data
        preprocessed = self.preprocessor.preprocess(input_data)
        
        # Model inference
        model_output = self.model_analyzer(preprocessed)
        
        # Postprocess model output
        result = self.postprocessor(model_output)
        
        return result
    


def main():
    from backend.inference_service.preprocess_manager import PreprocessManager
    from backend.inference_service.model_analyzer import ModelAnalyzer
    # Object initialization
    preprocessor = PreprocessManager()
    model_analyzer = ModelAnalyzer()

    def dummy_postprocessor(model_output):
        # Dummy postprocessor that just returns the model output
        return model_output

    pipeline_collector = PipelineController(preprocessor, model_analyzer, dummy_postprocessor)

    pipeline_collector.run("input data example")

if __name__ == "__main__":
    main()
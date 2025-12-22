class PipelineController:
    def __init__(self, preprocessor, model_analyzer, postprocessor):
        self.preprocessor = preprocessor
        self.model_analyzer = model_analyzer
        self.postprocessor = postprocessor
        
    def run(self, input_data):
        # Preprocess input data
        if isinstance(input_data, list):
            # Batch processing
            preprocessed = [self.preprocessor.preprocess(data) for data in input_data]
            # Model inference
            model_outputs = [self.model_analyzer(data) for data in preprocessed]
            # Postprocess model outputs
            result = self.postprocessor.postprocess_batch(model_outputs)
        else:
            # Single data processing
            preprocessed = self.preprocessor.preprocess(input_data)
            # Model inference
            model_output = self.model_analyzer(preprocessed)
            # Postprocess model output
            result = self.postprocessor(model_output)
            
        return result
    


def main():
    from backend.inference_service.preprocess_manager import PreprocessManager
    from backend.postprocess.PostprocessManager import PostprocessManager
    from backend.inference_service.model_analyzer import ModelAnalyzer
    # Object initialization
    preprocessor = PreprocessManager()
    model_analyzer = ModelAnalyzer()
    postprocessor = PostprocessManager()

    pipeline_collector = PipelineController(preprocessor, model_analyzer, postprocessor)

    pipeline_collector.run("input data example")

if __name__ == "__main__":
    main()
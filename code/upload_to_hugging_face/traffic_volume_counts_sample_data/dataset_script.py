import csv
import datasets

class GenericCSVLoader(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="Generic CSV loader script for Hugging Face Datasets.",
            features=datasets.Features({
                "RequestID": datasets.Value("string"),
                "Boro": datasets.Value("string"),
                "Yr": datasets.Value("string"),
                "M": datasets.Value("string"),
                "D": datasets.Value("string"),
                "HH": datasets.Value("string"),
                "MM": datasets.Value("string"),
                "Vol": datasets.Value("string"),
                "SegmentID": datasets.Value("string"),
                "WktGeom": datasets.Value("string"),
                "street": datasets.Value("string"),
                "fromSt": datasets.Value("string"),
                "toSt": datasets.Value("string"),
                "Direction": datasets.Value("string")
            }),
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager):
        data_path = dl_manager.download_and_extract("sample_traffic.csv")
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_path})
        ]

    def _generate_examples(self, filepath):
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                yield i, row

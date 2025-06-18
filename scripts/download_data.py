from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(
        'adarshsingh0903/legal-dataset-sc-judgments-india-19502024',
        path='data/',
        unzip=True
    )
    print("✅ Dataset downloaded and extracted.")


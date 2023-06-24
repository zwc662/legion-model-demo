# Deploy CodeT5P-770M model on Google Cloud

## Download model
1. Contact [Weichao Zhou](zwc662@gmail.com) for model files.
2. The model files at least include a `model.pt` file and a `tokenizer.json` file.
3. Create a `model` directory if it does not exsit and put all the model files under `model`.

## Build && Deploy

1. Open a terminal and activate a **zsh** shell by `$zsh`. 

2. Run command `make gcloud PROJECT_ID=${PROJECT_ID}` where `${PROJECT_ID}` is the ID of your project on google cloud. Type the following when prompted.
    * Type your app name, e.g., `test2sql`
    * Choose `30` for region
    * Choose `Y` when asked if allowing unauthenticated user (or 'N' depending on the situation)

3. Wait for a few seconds, open your browser and log into google cloud console. 
    * Go to `Cloud Run`, click into the app, e..g, `test2sql`, then click into `EDIT & DEPLOYMENT NEW REVISION`.
    * Edit the `Capacity` by allocting more memory (>= 4 GiB) and more CPU.
    * Scroll down to the bottom and click `Deploy`

## Test
1. Open your browser and log into google cloud console. Go to `Cloud Run`, click into the deployed app and find the app's url next to the app's name. 
2. Open your terminal and run command `python test.py ${URL}` where `URL` is the app's url.


### Reference

`https://huggingface.co/blog/how-to-deploy-a-pipeline-to-google-clouds`

PROJECT_ID=adept-mountain-380400
IMAGE_NAME=codet5p_770m
PARENT = $(notdir $(abspath $(CURDIR)/..))
local: 
	docker build . --tag ${IMAGE_NAME} -f ${PARENT}

gcloud: 
	gcloud config set project ${PROJECT_ID}
	gcloud builds submit --tag gcr.io/${PROJECT_ID}/${IMAGE_NAME} -f ${PARENT}
	gcloud run deploy --image gcr.io/${PROJECT_ID}/${IMAGE_NAME} --platform managed --allow-unauthenticated
 
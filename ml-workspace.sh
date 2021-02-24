docker run -d \
    -p 8080:8080 \
    --gpus all \
    --name "ml-workspace" -v "${PWD}/workspace:/workspace" \
    --env AUTHENTICATE_VIA_JUPYTER="password" \
    --shm-size 1024m \
    --restart always \
    mltooling/ml-workspace-gpu:latest

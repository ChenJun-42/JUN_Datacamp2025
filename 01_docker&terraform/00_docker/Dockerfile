# a image is blueprint for a container
# a container is a running instance of an image
# a image is a read-only template with instructions for creating a Docker container
# you can create multiple containers from the same image

# some docker commands:
# docker build -t <image_name> <path_to_dockerfile>
# docker run -it --entrypoint=bash <image_name>
# docker ps -a (list all containers)
# docker images (list all images)
# docker rm <container_id> (remove a container)
# docker rmi <image_id> (remove an image)
# docker exec -it <container_id> bash (run a command in a running container)

# set the base image for your docker container
FROM python:3.12

RUN pip install pandas

# sets the working directory inside the container.
# All subsequent commands(Run, cmd, copy, etc) will be run from this directory.
WORKDIR /app

# first one is source, second one is destination
COPY pipeline.py pipeline.py

# sets the default executable that runs when the container starts
# anything extra you add will be passed as command line arguments to the executable
# for example, if you run: docker run -it <image_name> hello world
# it will run: python pipeline.py hello world, and the argv[1:] will be ['hello', 'world']
ENTRYPOINT [ "python", "pipeline.py" ]

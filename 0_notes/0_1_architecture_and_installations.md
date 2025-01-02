
### Description  
This page contains main architecture diagram of data-engineering tools, techniques and pipelines and initial commands for 
installation packages

### Table of contents
1. [Install docker](#Install_docker)
2. [Create docker file](#create_docker_file)
3. [Build docker image](#build_docker_image)
4. [Run the docker image](#run_docker_image)

### Architecture diagram
![screenshot](0_notes/images/arch_v4_workshops.jpg)


### Action Items
1. Install docker <a name="Install_docker"></a>   
https://docs.docker.com/desktop/setup/install/mac-install/  
Test docker installation using following command 
    ```bash
    docker run hello-world
    ```
    ![screenshot](0_notes/images/docker-hello-run.png)  
    ![screenshot](0_notes/images/docker-bash-container-test.png)


2. Create docker file  <a name="create_docker_file"></a>  
Create Dockerfile in root dir with python 3.9 as base image and install pandas. Set entry 
point to run python script  

    ```text
   FROM python:3.9
   RUN pip install pandas
   WORKDIR  /app
   COPY data_pipeline_in_pandas.py data_pipeline_in_pandas.py
   ENTRYPOINT [ "python", "data_pipeline_in_pandas.py" ]
   # Default parameters
   CMD ["2025-01-01"]
   ```

3. Build docker image <a name="build_docker_image"></a>
    ```python
    docker build -t test:pandas .
    ```
   
4. Run the docker image <a name="run_docker_image"></a>
    ```python
    docker run -it test:pandas
    ```
   ![screenshot](0_notes/images/docker_package_and_run.png)

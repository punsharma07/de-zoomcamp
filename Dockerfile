FROM python:3.9
RUN pip install pandas
WORKDIR  /app
COPY data_pipeline_in_pandas.py data_pipeline_in_pandas.py
ENTRYPOINT [ "python", "data_pipeline_in_pandas.py" ]
# Default parameters
CMD ["2025-01-01"]
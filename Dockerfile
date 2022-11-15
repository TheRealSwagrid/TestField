FROM python
ENV semantix_port=7500

COPY TestField.py /var
COPY AbstractVirtualCapability.py /var
COPY requirements /var
RUN python -m pip install -r /var/requirements
EXPOSE 9999
CMD python /var/TestField.py ${semantix_port}
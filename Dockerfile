FROM python:3.7-alpine

ENV APP_ROOT=/opt/redeploy

WORKDIR ${APP_ROOT}

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD redeploy ./redeploy
ADD redeploy.py .

RUN addgroup -S redeploy && adduser -S -G redeploy redeploy
RUN chown -R redeploy:redeploy ${APP_ROOT}
USER redeploy

ENTRYPOINT ["python"]
CMD ["redeploy.py"]
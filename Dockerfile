ARG PYTHON_VERSION=3.12

# Production stage image
FROM python:${PYTHON_VERSION}-alpine AS builder
ENV PDM_CHECK_UPDATE=false
ARG PRJ_PATH=.
WORKDIR /tmp
RUN pip install -U pdm
# Use __pypackages__ , PEP 582
RUN pdm config python.use_venv False

ARG TARGETARCH
RUN --mount=type=cache,sharing=locked,id=${TARGETARCH}/var/cache/apk,target=/var/cache/apk \
    apk add gcc python3-dev libc-dev libffi-dev

# copy prj specific
COPY ${PRJ_PATH}/pyproject.toml ${PRJ_PATH}/pdm.lock ${PRJ_PATH}/pdm.toml ${PRJ_PATH}/README.md ./
RUN --mount=type=cache,target=/root/.cache/pdm,sharing=locked \
    pdm sync -G db --no-editable -v
    # pdm sync --prod --no-editable -v


# Production stage runner
FROM python:${PYTHON_VERSION}-alpine AS runner
ARG PRJ_PATH=.
WORKDIR /app
ENV PYTHONPATH=/opt/pkgs
COPY --from=builder /tmp/__pypackages__/*/lib ${PYTHONPATH}
COPY --from=builder /tmp/__pypackages__/*/bin/* /bin/
COPY ${PRJ_PATH}/public ./public
COPY ${PRJ_PATH}/assets ./assets
COPY ${PRJ_PATH}/src ./src
CMD ["uvicorn", "src.main:api", "--host", "0.0.0.0", "--port", "80"]

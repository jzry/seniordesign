# LitServe Model Server

For efficiency and better performance, [LitServe](https://lightning.ai/docs/litserve/home)
will be used to load and serve the image classifier model.

## Run It

To start serving the model, simply run the model server script:

`python model_server.py`

## Disable LitServe

By default, the OCR will always attempt to connect to the LitServe server.
You can configure the OCR to bypass LitServe by setting the environment variable
[`BYPASS_LITSERVE`](../ENV.md#bypass_litserve).

## Configuration

LitServe can be configured by setting these environment variables in the `.env` file.

- [`LITSERVE_PORT`](../ENV.md#litserve_port) Configure which port LitServe will use.
- [`LITSERVE_URL`](../ENV.md#litserve_url) Configure the URL at which LitServe can be accessed.
- [`LIT_SERVER_API_KEY`](../ENV.md#lit_server_api_key) Configure password authentication for LitServe requests.

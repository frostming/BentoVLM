# VLM Parsing Example Bento

[![BentoML](https://img.shields.io/badge/BentoML-1.3.14-4dad8c)](https://bentoml.com)
[![pdm-managed](https://img.shields.io/endpoint?url=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2Fpdm-project%2F.github%2Fbadge.json)](https://pdm-project.org)

This is a BentoML service that demonstrates how to parse image using multi-modal LLM and extract useful information from them.

_The work is based on @PsiACE's [blog post](https://psiace.me/posts/a-dead-simple-way-to-vlm-parsing/)._

## Start the development server

This project is managed by [PDM](https://pdm-project.org), install it first.

Install dependencies:

```bash
pdm install
```

Create `.env` file with credentials:

```bash
cp .env.example .env
# Complete the OPENAI_API_KEY in the .env file
```

Start the development server:

```bash
pdm dev
```

## Deploy to BentoCloud

1. Go to [BentoCloud](https://cloud.bentoml.com) and get an account.
2. Login to BentoCloud:

   ```bash
   pdm run bentoml cloud login
   ```
3. Click "Secret" in the sidebar and create an "OpenAI" secret with your API key.

4. Deploy the service to BentoCloud:

   ```bash
   pdm deploy --secret <your-secret-name>
   ```

![Bento Cloud](image.png)


## License

This work is released under [Unlicense](LICENSE). You can use it for any purpose without any restriction.


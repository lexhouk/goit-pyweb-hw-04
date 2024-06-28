# Web application

## Deployment

```bash
$ docker buildx b -t oleksandr-horbatiuk/goit-pyweb-hw-04 .
$ docker run --name oleksandr-horbatiuk-goit-pyweb-hw-04 -p 3000:3000 -v ./front-init/storage:/app/front-init/storage -d oleksandr-horbatiuk/goit-pyweb-hw-04
```

# Usage

Go to http://localhost:3000.

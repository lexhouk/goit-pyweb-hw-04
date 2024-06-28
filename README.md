# Web application

## Deployment

```bash
$ docker buildx b -t lexhouk/goit-pyweb-hw-04 .
$ docker run --name lexhouk-hw-04 -p 3000:3000 -v ./www/storage:/app/www/storage -d lexhouk/goit-pyweb-hw-04
```

## Usage

Go to http://localhost:3000.

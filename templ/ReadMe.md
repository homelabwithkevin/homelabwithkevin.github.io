# Read Me
Website with templ, tailwindcss, and AWS Cloudfront + AWS S3.

# CLI
## Tailwind
npx tailwindcss -i ./src/input.css -o ./src/tailwind.css --watch

## Deploy
### Linux
```bash
    templ generate && rm -rf public/ && go run *.go && cp ./src/tailwind.css ./public/css/tailwind.css
```

### Windows
```powershell
    templ generate; del .\public\; go run .; copy .\src\tailwind.css .\public\css\tailwind.css
```

## AWS
aws s3 sync public/ s3://homelabwithkevin.com

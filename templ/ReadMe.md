# Read Me
Website with templ, tailwindcss, and AWS Cloudfront + AWS S3.

# CLI
## Tailwind
npx tailwindcss -i ./src/input.css -o ./src/tailwind.css --watch

## Deploy
templ generate && rm -rf public/ && go run *.go && cp ./src/tailwind.css ./public/css/tailwind.css

## AWS
aws s3 sync public/ s3://homelabwithkevin.com

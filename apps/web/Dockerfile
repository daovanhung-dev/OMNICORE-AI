FROM node:24-alpine AS build

WORKDIR /workspace
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /workspace/dist/web/browser /usr/share/nginx/html
EXPOSE 80

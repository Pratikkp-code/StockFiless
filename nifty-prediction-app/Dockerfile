# Build stage
FROM node:16-alpine as build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine

# Install envsubst to allow runtime variable substitution
RUN apk add --no-cache bash gettext

# Copy built app from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx config template (keep ${API_URL} placeholder inside)
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Expose port
EXPOSE 80

# Entry point: substitute API_URL into nginx config at container startup
CMD ["/bin/sh", "-c", "envsubst '$API_URL' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"]

FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

# El código fuente se monta como volumen en desarrollo.
# En producción: agregar COPY . . y RUN npm run build con CMD npm start.

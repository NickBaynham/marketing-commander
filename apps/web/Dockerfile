# Marketing Commander web stub container (Phase 3, Increment 3.4).
# node:24-alpine is the active Node LTS line, pinned per plan decision
# D3-1. Development-mode container: compose bind-mounts the source over
# /app (with node_modules kept in an anonymous volume) and `next dev`
# hot-reloads edits without a rebuild.
FROM node:24-alpine

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]

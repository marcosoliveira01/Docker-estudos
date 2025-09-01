# 🐳 Docker Estudos

Repositório de estudos com Docker. Aqui vou arquivar todos os projetos que fiz utilizando Docker, desde os mais básicos até os mais avançados.

## 📁 Estrutura do Repositório

### Projetos Básicos (`Basicos/`)

- **`Projeto1/`** → Aplicação Go simples com servidor HTTP
  - Servidor web "Hello, World!" em Go
  - Dockerfile multi-stage para build otimizado
  - Container Alpine Linux para produção

- **`projeto2/`** → Aplicação Node.js completa com frontend e backend
  - Frontend React com Vite
  - Backend Node.js com API REST
  - Dockerfile multi-stage para desenvolvimento e produção
  - Docker Compose para orquestração

- **`streamlit-app/`** → Aplicação Python com Streamlit
  - App web interativo com Streamlit
  - Dependências: pandas, numpy
  - Docker Compose para desenvolvimento
  - Healthcheck configurado

## 🛠️ Tecnologias & Ferramentas

- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Linguagens**: Go, JavaScript/Node.js, Python
- **Frameworks**: React, Vite, Streamlit
- **Imagens base**: golang:alpine, node, python:slim, alpine

## 🎯 Objetivo

- ✅ Consolidar conceitos básicos do Docker
- ✅ Praticar criação e customização de imagens
- ✅ Gerenciar containers de forma eficiente
- ✅ Estudar casos reais com **Docker Compose**
- 🔄 Futuramente estudar **Kubernetes**

## 🚀 Como usar

### Projeto1 (Go)
```bash
cd Basicos/Projeto1
docker build -t projeto1 .
docker run -p 8080:8080 projeto1
```

### Projeto2 (Node.js Full Stack)
```bash
cd Basicos/Projeto1/projeto2
docker build -t projeto2 .
# ou usar compose:
docker-compose up --build
```

### Streamlit App (Python)
```bash
cd Basicos/streamlit-app
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
# ou para desenvolvimento:
docker-compose -f compose.dev.yml up --build
```

## 📊 Status dos Projetos

| Projeto | Status | Tecnologia | Container | Funcionando |
|---------|--------|------------|-----------|-------------|
| Projeto1 | ✅ | Go | Alpine | ✅ |
| projeto2 | ✅ | Node.js | Multi-stage | ✅ |
| streamlit-app | ✅ | Python/Streamlit | Slim | ✅ |

---

> 💡 **Nota**: Todos os projetos incluem Dockerfiles otimizados e estão funcionais para estudo e desenvolvimento.

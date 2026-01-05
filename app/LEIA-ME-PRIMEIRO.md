# ⚠️ LEIA-ME PRIMEIRO - Projeto DIVA API

## � PROJETO FINALIZADO COM SUCESSO!

Sua API de Cibersegurança foi completamente reorganizada e documentada.

---

## 🚀 Comece Aqui (3 Passos)

### 1️⃣ Instale as Dependências

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure o .env

Crie um arquivo `.env` na pasta raiz com:
```
DB_HOST=localhost
DB_USERNAME=root
DB_PASSWORD=sua_senha
DB_DATABASE=cybersecurity_threats
```

### 3️⃣ Execute a API

```bash
python app\main.py
```

Acesse: **http://localhost:5000/apidocs** ⭐

---

## ✅ O Que Foi Feito

✓ **Modernizado:** Interface Swagger com novo design profissional
✓ **Documentado:** Guias completos em `documentacao-api/`
✓ **Testado:** Script `testar_api.py` para validar funcionalidades
✓ **Organizado:** Estrutura limpa e profissional

---

## 📚 Documentação por Caso de Uso

### 🔧 Para INSTALAR e CONFIGURAR:
→ **documentacao-api/GUIA_INSTALACAO.md**

### 📖 Para ENTENDER as ROTAS:
→ **documentacao-api/ROTAS_DISPONIVEIS.md**

### 🏗️ Para APRENDER a ARQUITETURA:
→ **documentacao-api/construção-da-api.md** (Explicação didática!)

### 🧪 Para TESTAR no Postman:
→ **documentacao-api/Flask_crud.postman_collection.json**

### 🚀 Para TESTAR via CLI:
→ Após iniciar a API: `python testar_api.py`

---

## 📁 Estrutura do Projeto

```
flask-crud/
├── app/                      ← Sua aplicação (4-layer pattern)
├── documentacao-api/         ← 📚 Toda documentação organizada
├── requirements.txt          ← Dependências (inclui requests)
├── testar_api.py            ← Script de teste HTTP
├── README.md                ← Documentação principal
└── .env                     ← Configuração (NÃO commit!)
```

---

## 🆘 Problemas?

**"Module not found" (requests, flask, etc)**
→ Execute: `pip install -r requirements.txt`

**"Access denied" (MySQL)**
→ Verifique user/password no .env

**"Database not found"**
→ Crie a base de dados conforme `documentacao-api/GUIA_INSTALACAO.md`

---

## 🎯 Próximos Passos

1. Ative o ambiente virtual
2. Instale as dependências
3. Configure o .env
4. Execute: `python app\main.py`
5. Abra: http://localhost:5000/apidocs
6. Teste as rotas no navegador
7. Leia `documentacao-api/construção-da-api.md` para entender tudo

---

## 📞 Informações Úteis

- **API URL:** http://localhost:5000
- **Docs:** http://localhost:5000/apidocs
- **Rotas:** 36 endpoints em 6 categorias
- **Métodos:** GET, POST, PUT, DELETE
- **Autenticação:** Sem autenticação (desenvolvimento)

---

**Pronto para usar!** 🛡️ Comece pelo passo 1 acima.






require("dotenv").config();
const express = require("express");
const filmeRoutes = require("./routes/filmeRoutes");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware para parsear JSON
app.use(express.json());

// Middleware para parsear dados URL-encoded
app.use(express.urlencoded({ extended: true }));

// Rota de health check
app.get("/health", (req, res) => {
  return res.status(200).json({
    statusCode: 200,
    message: "API está online e funcionando",
    timestamp: new Date().toISOString(),
  });
});

// Rotas da API
app.use("/v1/controle-filmes", filmeRoutes);

// Tratamento de rotas não encontradas (404)
app.use((req, res) => {
  return res.status(404).json({
    statusCode: 404,
    message: "Rota não encontrada",
    path: req.path,
  });
});

// Tratamento de erros genérico
app.use((err, req, res, next) => {
  console.error("Erro não tratado:", err);
  return res.status(500).json({
    statusCode: 500,
    message: "Erro interno do servidor",
    error: err.message,
  });
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`

*****************************************************
*       🎬 UniFECAF Flix API está rodando! 🎬      *
*****************************************************
* Servidor: http://localhost:${PORT}
* Ambiente: ${process.env.NODE_ENV || "development"}
* Health Check: http://localhost:${PORT}/health
*****************************************************
  `);
});

module.exports = app;

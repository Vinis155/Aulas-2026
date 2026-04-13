const express = require("express");
const router = express.Router();
const filmeController = require("../controllers/filmeController");

// GET /v1/controle-filmes/filme - Listar todos os filmes
router.get("/filme", filmeController.listarTodos);

// GET /v1/controle-filmes/filme/:id - Buscar filme por ID
router.get("/filme/:id", filmeController.buscarPorId);

// GET /v1/controle-filmes/filtro/filme - Filtrar filmes
router.get("/filtro/filme", filmeController.filtrar);

module.exports = router;

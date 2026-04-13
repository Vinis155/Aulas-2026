const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

// Listar todos os filmes
exports.listarTodos = async (req, res) => {
  try {
    const filmes = await prisma.filme.findMany();
    return res.status(200).json({
      statusCode: 200,
      message: "Filmes recuperados com sucesso",
      data: filmes,
    });
  } catch (error) {
    console.error("Erro ao listar filmes:", error);
    return res.status(500).json({
      statusCode: 500,
      message: "Erro ao listar filmes",
      error: error.message,
    });
  }
};

// Buscar filme por ID
exports.buscarPorId = async (req, res) => {
  try {
    const { id } = req.params;
    const idConvertido = parseInt(id, 10);

    // Validar se o ID é um número válido
    if (isNaN(idConvertido)) {
      return res.status(400).json({
        statusCode: 400,
        message: "ID deve ser um número inteiro válido",
      });
    }

    const filme = await prisma.filme.findUnique({
      where: { id: idConvertido },
    });

    if (!filme) {
      return res.status(404).json({
        statusCode: 404,
        message: `Filme com ID ${idConvertido} não encontrado`,
      });
    }

    return res.status(200).json({
      statusCode: 200,
      message: "Filme encontrado com sucesso",
      data: filme,
    });
  } catch (error) {
    console.error("Erro ao buscar filme por ID:", error);
    return res.status(500).json({
      statusCode: 500,
      message: "Erro ao buscar filme",
      error: error.message,
    });
  }
};

// Filtrar filmes por nome ou sinopse
exports.filtrar = async (req, res) => {
  try {
    const { nome } = req.query;

    if (!nome || nome.trim() === "") {
      return res.status(400).json({
        statusCode: 400,
        message: "Parâmetro 'nome' é obrigatório e não pode ser vazio",
      });
    }

    const filmes = await prisma.filme.findMany({
      where: {
        OR: [
          {
            nome: {
              contains: nome,
              mode: "insensitive",
            },
          },
          {
            sinopse: {
              contains: nome,
              mode: "insensitive",
            },
          },
        ],
      },
    });

    return res.status(200).json({
      statusCode: 200,
      message: `Filmes encontrados com o termo "${nome}"`,
      data: filmes,
      total: filmes.length,
    });
  } catch (error) {
    console.error("Erro ao filtrar filmes:", error);
    return res.status(500).json({
      statusCode: 500,
      message: "Erro ao filtrar filmes",
      error: error.message,
    });
  }
};

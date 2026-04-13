const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

// Função auxiliar para validar dados de entrada
const validarFilme = (nome, sinopse, duracao, genero) => {
  const erros = [];

  if (!nome || typeof nome !== "string" || nome.trim() === "") {
    erros.push("Nome é obrigatório e deve ser uma string");
  }

  if (!sinopse || typeof sinopse !== "string" || sinopse.trim() === "") {
    erros.push("Sinopse é obrigatória e deve ser uma string");
  }

  if (!duracao || isNaN(parseInt(duracao)) || parseInt(duracao) <= 0) {
    erros.push("Duração é obrigatória e deve ser um número positivo");
  }

  if (!genero || typeof genero !== "string" || genero.trim() === "") {
    erros.push("Gênero é obrigatório e deve ser uma string");
  }

  return erros;
};

// Criar novo filme
exports.criar = async (nome, sinopse, duracao, genero, capaUrl = null) => {
  try {
    const erros = validarFilme(nome, sinopse, duracao, genero);
    if (erros.length > 0) {
      throw new Error(erros.join("; "));
    }

    const filme = await prisma.filme.create({
      data: {
        nome: nome.trim(),
        sinopse: sinopse.trim(),
        duracao: parseInt(duracao),
        genero: genero.trim(),
        capaUrl: capaUrl ? capaUrl.trim() : null,
      },
    });

    return filme;
  } catch (error) {
    throw error;
  }
};

// Atualizar filme
exports.atualizar = async (id, dados) => {
  try {
    const filme = await prisma.filme.update({
      where: { id: id },
      data: {
        ...dados,
      },
    });

    return filme;
  } catch (error) {
    throw error;
  }
};

// Deletar filme
exports.deletar = async (id) => {
  try {
    await prisma.filme.delete({
      where: { id: id },
    });

    return { success: true };
  } catch (error) {
    throw error;
  }
};

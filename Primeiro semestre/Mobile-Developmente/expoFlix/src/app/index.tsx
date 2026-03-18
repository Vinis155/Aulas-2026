import { InputComponent } from "@/components/inputComponent";
import { useRouter, type Href } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useState } from "react";
import { Text, View, StyleSheet, TouchableOpacity } from "react-native";

export default function Login() {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [isError, setIsError] = useState<string>("");

  const router = useRouter();

  //FAZER A LÓGICA PARA NAVEGAR PARA O DASHBOARD
  const handlerLogin = () => {
    //REGRAS PARA IR PARA A PRÓXIMA TELA
    //1 - OS CAMPOS NÃO PODEM FICAR VAZIOS
    if (email === "" || password === "") {
      setIsError("Preencha todos os campos");
      return;
      
    }
    //2 - O EMAIL DEVE SER UM EMAIL VÁLIDO, OU SEJA, VERIFICAR SE TEM O '@' NO TEXTO
     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
     if (!emailRegex.test(email)) {
       setIsError("Digite um email válido");
       return;
    }
    //3 - A SENHA DEVE TER NO MINIMO 6 CARACTERES
    if (password.length < 6) {
      setIsError("A senha deve conter no mínimo 6 caracteres");
      return;
    }
    //4 - USUÁRIO E SENHA DEVE SER IGUAL A: boanoite.punpun@gmail.com e BoanoitePunpun
    if (email !== "boanoite.punpun@gmail.com" || password !== "BoanoitePunpun") {
      setIsError("Email ou senha incorretos");
      return;
    }

    //5 - APÓS CONTEMPLAR TODAS AS REGRAS, FAZER A NAVEGAÇÃO PARA A PRÓXIMA TELA
    //CASO ALGUMA REGRA SEJA QUEBRADA, DEVE APARECER UMA MENSAGEM DE ERRO.
    router.replace("/(tabs)/dashboard" as Href);
  };

  //NOTE QUE TEMOS UMA TAG CHAMADA 'InputComponent'. ESSE COMPONENTE ESTA NA PASTA COMPONENTE.
  //VÁ ATÉ A PASTA COMPONENTE E COMPLETE O CÓDIGO DO ARQUIVO PARA QUE FUNCIONE.

  return (
    <View style={styles.container}>
      <Text style={styles.title}>ExpoFlix</Text>
      <InputComponent
        label="Email"
        placeholder="Digite o Email"
        type="email-address"
        value={email}
        setValue={setEmail}
      />
      <InputComponent
        label="Senha"
        placeholder="Digite a Senha"
        type="default"
        value={password}
        setValue={setPassword}
      />
      {isError && <Text style={styles.errorMessage}>{isError}</Text>}
      <TouchableOpacity style={styles.button} onPress={handlerLogin}>
        <Text style={styles.buttonTitle}>Entrar</Text>
      </TouchableOpacity>
      <StatusBar style="auto" hidden />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#19244B",
  },
  title: {
    color: "white",
    fontSize: 32,
    fontWeight: "600",
    marginBottom: 24,
  },
  input: {
    backgroundColor: "white",
    width: 300,
    height: 40,
    padding: 4,
    borderWidth: 1,
    borderColor: "#6B76A0",
    borderRadius: 8,
  },
  errorMessage: {
    alignSelf: "center",
    color: "#F5482F",
  },
  button: {
    backgroundColor: "#86A16C",
    width: 300,
    height: 40,
    marginTop: 30,
    borderRadius: 8,
    justifyContent: "center",
    alignItems: "center",
  },
  buttonTitle: {
    color: "#fff",
    fontWeight: "400",
    fontSize: 16,
  },
});

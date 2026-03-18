import {
  TextInput,
  StyleSheet,
  Text,
  KeyboardAvoidingView,
} from "react-native";

//COMPLETE OS TIPOS QUE ESTÃO FALTANDO NO PROPS
type Props = {
  placeholder: string; 
  label: string;
  type: "email-address" | "default";
  value: string;
  setValue: (data: string) => void;
};

//COMPLETE OS PROPS DENTRO DO TextInput. PREENCHA CORRETAMENTE. E INSIRA O NOME DOS CAMPOS. 
//LEMBRANDO QUE TODAS AS INFORMAÇÕES ESTÃO VINDO DO COMPONENTE PAI. AS INFORMAÇÕES TEM QUE SER DINÂMICAS.
export const InputComponent = ({
  placeholder,
  label,
  type,
  value,
  setValue,
}: Props) => {
  return (
    <KeyboardAvoidingView>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        style={styles.input}
        placeholder={placeholder}
        autoCapitalize="none"
        keyboardType={type}
        value={value}
        onChangeText={(data: string) => setValue(data)}
      />
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  label: {
    color: "#fff",
    marginBottom: 5,
    fontSize: 16,
    fontWeight: "500",
  },
  input: {
    backgroundColor: "white",
    width: 300,
    height: 40,
    padding: 4,
    borderWidth: 1,
    borderColor: "#6B76A0",
    borderRadius: 8,
    marginBottom: 15,
  },
});

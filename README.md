# 🏥 **CLINICA VIDA+ - Sistema de Gestão de Clínicas (Desktop App)** 🏥 

## Visão Geral do Projeto
Este é um sistema desktop completo para o Gerenciamento de Pacientes e Médicos. Desenvolvi ele em Python, usando o PyQt5 para a interface gráfica e o SQLite como nosso "cérebro" para guardar tudo.
A ideia foi criar uma ferramenta pronta para usar, que não dependa de servidor e resolva a vida de clínicas pequenas ou consultórios. O foco foi duplo: fazer funcionar 
(persistência de dados segura) e fazer ficar bom (cuidado com a usabilidade e Pequenos erros). É o meu projeto para ir muito além do que foi pedido na faculdade.

## Exemplos do sistema - Menu principal, tela de cadastro, medicos e Dados.
<img width="270" height="270" alt="image" src="https://github.com/user-attachments/assets/85981e1a-0428-407d-baca-ff260c06ea65" />	<img width="275" height="270" alt="image" src="https://github.com/user-attachments/assets/0eb8f730-41f7-4398-9df3-7d6aec04d7a0" />	 <img width="270" height="270" alt="image" src="https://github.com/user-attachments/assets/1b8ae2ad-7bf8-493d-aaa7-ffbcb10efa18" />
<img width="270" height="270" alt="image" src="https://github.com/user-attachments/assets/2361598e-f26d-45f1-99e4-5ee938cd0331" />	<img width="270" height="270" alt="image" src="https://github.com/user-attachments/assets/c1175c22-6fde-4b2c-ba26-a7a5afd8bf56" />  <img width="270" height="270" alt="image" src="https://github.com/user-attachments/assets/c03d75b2-9ef9-484e-a771-0b56b2741577" />

## Principais Funcionalidades
O sistema é robusto e dividido em módulos claros:

 Gestão de Cadastros (Admin) e Gestão de Pacientes: Criar, editar e remover pacientes. Os dados essenciais (Nome, CPF, Telefone e Idade) ficam armazenados com segurança.	                                              
Gestão de Médicos: Mesmo esquema para os médicos, definindo Nome, Área e Idade. Importante: O CRM tem uma validação para garantir que não existam duplicidades.

## Controle de Fluxo
Fila de Atendimento, Controle de entrada com registro de horario e Simulacao de atendimento para que com clique duplo
pode remover o paciente da fila, como se ja tivesse sido atendido e libera o fluxo.

## Validação e Persistência
Persistência com SQLite: Todos os dados ficam salvos localmente no arquivo .db, ou seja, o sistema lembra de tudo quando você reabre.
Validação de Formulários: Implementei tratamento de erros para garantir que ninguém cadastre letra no campo de CPF ou números no campo Nome.

  ## Tecnologias Utilizadas
● `Linguagem utilizada ● Python 3.11.1 ● Lógica de programação, POO e backend local.`                                      
● `Interface Gráfica ● PyQt5 ● Framework para desenvolvimento de aplicações desktop nativas (GUI).`                                       
● `Banco de Dados ● SQLite3 ● Banco de dados relacional leve para armazenamento de registros. `                                      
● ` Estilização ● QSS (Qt Style Sheets) ● Design customizado para aplicação do tema escuro/profissional.  `                                     

## Como Executar o Projeto
Este projeto é um aplicativo desktop e roda localmente.

Pré-requisitos: Certifique-se de ter o Python 3.11.1 instalado.

Clonar o Repositório (no terminal) :                                              
●                                      ``git clone https://github.com/peeerimbr5/programa_clinica``                                             
Instalar as dependencias (no terminal) :                                              
●                                      `cd programa_clinica`                                                                                          
Executar o programa (no terminal) :	                                                                
●                                      ` pyhton minhainterface.py `

O arquivo do banco de dados (clinica_vidamais.db) e as tabelas necessárias são criados automaticamente na primeira execução do script.



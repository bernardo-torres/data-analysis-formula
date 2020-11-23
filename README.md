# Data Analysis Formula UFMG
## Objetivo
O objetivo desse projeto é fornecer uma ferramenta para a análise dos dados coletados pela equipe Formula SAE UFMG. O programa surge inicialmente como uma ferramenta de transição, permitindo que o usuário importe os logs gravados durante uma sessão de testes e aplique correções e análises preliminares nos dados. É possível exportar esse resultado para um arquivo .csv e também para o formato .dlf, utilizado por exemplo pelo software Pro Tune Analyzer. O usuário consegue também aplicar filtros e visualizar o resultado, assim como o sinal original.

## Como utilizar
### Arquivos

Baixe os arquivos do repositório. O executável do programa se encontra na pasta *dist*, com o nome analise.exe. Recomendo criar um atalho para esse .exe caso não queira abrir essa pasta sempre que for utilizar o programa. Para executar e utilizar o programa, só é necessário baixar a pasta *dist*.

As pastas *Txts competicao 2018* e *Mais txts* contem arquivos .txts de exemplo no formato aceito pelo programa e funcionando (fev/2020).
### Pré-requisitos

Na versão atual, não há pré-requisitos para utilizar o executável. Para desenvolvimento ou para rodar os scripts .py, sem utilizar o executável, veja [Desenvolvimento](#desenvolvimento).

### Utilizando o programa

![print](/images/print.png)

O botao *abrir* permite que o usuário escolha um .txt. Caso um log já tenha sido carregado, é possível exportar para um arquivo .csv as informacoes contidas no gráfico. Serao exportados somente os dados plotados no gráfico, com as respectivas modificacoes, caso tenham sido feitas, como adicao de offset, multiplicacao por algum valor e filtros, além de uma coluna com os valores de tempo. (22/07) É possível também exportar os dados para o formato utilizado pelo software Pro Tune Analyzer: basta utilizar a ferramenta "Exportar pro tune" do mesmo botão *arquivo*, e todos os dados contidos no .txt original serao exportados (não somente os que estão plotados no gráfico, como no caso do export para .csv).

Ao lado, o botao Figura permite que sejam adicionados nomes aos eixos e um título ao gráfico.

O botao aplicar funções permite que o usuário escolha, ao abrir um arquivo, se serao aplicadas as funcoes de calibracao ou se os dados serao mostrados na forma como foram enviados pelo carro.

Para plotar um dado, clique duas vezes no seu nome da lista. Para remove-lo, clique duas vezes em seu nome novamente. Para resetar o estado da figura, clique em limpar figura.

Dentro da aba da figura, na parte superior, é possível modificar os dados que serao inseridos. É possível multiplicar o dado por um valor e adicionar um offset.

O filtro Hampel é um removedor de outliers. Seu parametro *janela* indica com quantos pontos ao redor do ponto avaliado será calculada a média. O valor *K* é um valor de *threshold*, que indica que a partir de uma distancia de *K* desvios padroes da média, o ponto será retirado e substituído pela média.

O filtro Savitzky-Golay é utilizado para suavizar a curva. Ele funciona como uma média móvel generalizada, na qual é possível variar também a ordem do polinomio utilizado para interpolar os pontos da janela. Uma média móvel é um Savitzky-Golay de ordem 0. [Savitzky-Golay](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter/).

Na Figura acima, foi plotado uma posicao angular do volante com e sem um filtro Savitzky-Golay e, no mesmo gráfico, uma aceleracao lateral multiplicada por 100 e com um offset de -200.

Os efeitos mencionados só sao aplicados aos **novos** dados inseridos, ou seja, se um dado já está plotado, ele nao vai mudar. É importante lembrar de **desmarcar as caixas de selecao dos filtros e resetar os valores de multiplicadores e offsets para 1 e 0, respectivamente**, antes de inserir outro dado, pois esses efeitos serao aplicados a todos os dados que forem adicionados.

Na parte inferior encontram-se ferramentas para manipular o gráfico, como zoom  e selecao. É possível também modificar a cor e o estilo das curvas, assim como salvar a imagem.

### Formato do .txt de entradas

Espera-se como entrada um .txt que possua o formato mostrado abaixo nas primeiras linhas.
Nao tem problema adicionar comentários ou outras linhas entre os dois \*\*\*.
As seguintes linhas sao essenciais, e devem ser mantidas exatamente da mesma forma como o exemplo abaixo:
 -  Posicao maxima e minima do volante
 - PACOTEN TAXA LISTADEDADOS VARIAVELTEMPORAL

As linhas que informam a ordem dos dados recebidos deve iniciar com PACOTEN, onde N é o numero do pacote. Em seguida, a taxa de envio em Hz. Depois, separadas por espacos, os nomes das variaveis, até a última variavel que é a variável de tempo

```
***
CARRO: TR-06
PISTA: autocross - ECPA
PILOTO: cambraia
TEMPERATURA AMBIENTE:
ANTIROLL:
PRESSÃO PNEUS DIANTEIROS:
PRESSÃO PNEUS TASEIROS:
ÂNGULO DE ATAQUE DA ASA:
MAPA MOTOR:
BALANCE BAR:
DIFERENCIAL:
COMENTÁRIOS: Passada 1 - 2018. Fs = 40Hz
PACOTE1 40 acelY acelX acelZ velDD sparkCut suspPos time
PACOTE2 20 oleoP fuelP tps rearBrakeP frontBrakeP volPos beacon correnteBat time2
PACOTE3 2 ect batVoltage releBomba releVent pduTemp tempDiscoD tempDiscoE time3
PACOTE4 20 ext1 ext2 ext3 time4
***

1 14736 -5034 14350 53 0 0 14392
2 4574 2941 831 229 249 2196 1 2034 14392
```
### Funcoes de calibracao

As funcoes de calibracao podem ser modificadas pelo usuário. A configuracao dos valores das funcoes é feita por meio do arquivo *functions.txt*, localizado **na mesma pasta que o arquivo executável, dentro de /dist/analise**.

O arquivo possui o formato:
```
acelX mult 0.0000610351 0 g
acelY mult 0.0000610351 0 g
acelZ mult 0.0000610351 0 g
velT mult 1 0 km/h
sparkCut mult 1 0 -
suspPos lin 5000 0 240 120 -
oleoP mult 0.001 0 bar
fuelP mult 0.001 0 bar
```
Na primeira coluna temos o nome da variável, que tem que ser o mesmo nome colocado no .txt da entrada para que ela possa ser mostrada no gráfico em sua escala correta. Considerando o arquivo de configuracao de exemplo acima, se no .txt de entrada há a seguinte linha:
```
PACOTE1 40 acelY acelX aceleracaoZ velDD sparkCut suspPos time
```
Todos os dados, exceto o *aceleracaoZ*, estariam em suas escalas corretas, pois há correspondencia de nomes com o arquivo de configuracao das funcoes de calibracao.

Para modificar, basta editar o valor desejado (ou inserir uma linha) e salvar o arquivo.

A segunda coluna pode conter dois valores: **mult** ou **lin**. Uma linha com **mult**, na forma:
```
nomeDoDado mult A B unidade
```
Terá sua funcao na forma:
```
Valor na escala correta = valor gravado * A + B
```
Ou seja, o primeiro numero (A) é o multiplicador e (B) o offset.

Uma linha com **lin**, na forma:
```
nomeDoDado lin max min range offset unidade
```
Terá sua funcao na forma:
```
Valor na escala correta =  (valor gravado - MAX) * range/(MAX-MIN) - offset
```
A última coluna sempre contém a unidade de engenharia do dado. Se não houver unidade, colocar um hífen (-)
## Desenvolvimento
### Dependencias
Dependencias para desenvolvimento

```
matplotlib - pip install matplotlib
numpy - pip install numpy
pyqt5-tools - pip install pyqt5-tools
PyQt5
pyqtgraph - pip install pyqtgraph
pandas - pip install pandas
```

O pyqt5-tools instala também o Qt Designer, ferramenta utilizada para criar o visual da interface

### Modificando a interface

Para modificar algo na interface, altere o arquivo interface.ui, salve, e execute o seguinte comando:

```
pyuic5 -x dataAnalysisGui.ui -o guiGenerated.py
```

Após executar o comando, procure a linha <from pyqtgraph import PlotWidget>, no arquivo interface_generated.py,
(deve estar antes da declaracao <if __name__ == "__main__":>, no fim do arquivo), recorte ela e cole após a
declaracao <from PyQt5 import QtCore, QtGui, QtWidgets>, no inicio do arquivo. Isso deve ser feito após qualquer
alteracao no Qt Designer para que ela tenha efeito no codigo, de forma a evitar o erro no qual nao é reconhecido o modulo pyqtgraph.

### Pyinstaller (executavel)
```
pyinstaller --add-data "functions.txt;." analise.py
```
## Próximas modificações
- [x] Reescrever runAnalysis utilizando pandas (29/05)
- [X] Adicionar export para arquivo do Pro Tune (22/07)
- [ ] Adicionar import de csv
- [ ] Reset mais inteligente das cores do gráfico
- [ ] Adicionar input manual das freqs de aquisição na interface
- [ ] Adicionar opção de resample para outras frequencias
- [ ] Erro quando o usuario tenta exportar mais nao ha dados
- [ ] Mostrar quais pontos foram perdidos

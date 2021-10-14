

function adm_reportar_erro(cod_aux, des, tip, id_btn, op_funcao_retorno) {
    /*
    alert("chegou no adm_reportar_erro");
    alert("cod_aux:  " + cod_aux);
    alert("des: " + des);
    alert("tip: " + tip);
    alert("id_btn: " + id_btn);
    alert("op_funcao_retorno: " + op_funcao_retorno);
    */


    if (!hasValue(des.trim())) return false;

    if ($("#" + id_btn).hasClass("botao_buffering")) return false;

    $("#" + id_btn).val(' ');
    $("#" + id_btn).addClass("botao_buffering");


    $.ajax({

        data: {
            cod_fii: window.cod_fii_numerico,
            cod_aux: cod_aux,
            des: des,
            tip: tip,
        },

        type: "post",
        url: "/processamentos?adm_reportar_erro=true",
        success: function (data) {
            $("#" + id_btn).removeClass("botao_buffering");
            $("#" + id_btn).val('ENVIAR');

            $("#conteudo_reportar_erro_" + cod_aux).hide();
            $("#lbl_erro_enviado_" + cod_aux).show();


            if (hasValue(op_funcao_retorno)) {
                var fnc_retorno_reportar_erro = new Function(op_funcao_retorno);
                fnc_fnc_retorno_reportar_erro();
            }

        }
    });

}

      function toogle_itens_menu(div_itens_menu)
      {
          if (!hasValue($("#menu_itens_" + div_itens_menu).attr("itemid"))
              || $("#menu_itens_" + div_itens_menu).attr("itemid") == 'false')
          {
              $("#menu_itens_" + div_itens_menu).attr("itemid", 'true');
              $("#menu_itens_" + div_itens_menu).slideDown();
              $("#seta_direita_" + div_itens_menu).hide();
              $("#seta_baixo_" + div_itens_menu).show();
          }
          else
          {
              $("#menu_itens_" + div_itens_menu).attr("itemid", 'false');
              $("#menu_itens_" + div_itens_menu).slideUp(500);
              $("#seta_direita_" + div_itens_menu).show();
              $("#seta_baixo_" + div_itens_menu).hide();
          }
      }



function inscrever_usuario_evento_universal(fnc_retorno, cod_hor, status) {
    //  if (!hasValue(cod_pro)) cod_pro = 0

  //  if
   // new Function("alert('blabla')");
    if (fnc_retorno != '') fnc_retorno = new Function(fnc_retorno);



    $.post("/inserir_dado?tipo_dado=curso_inscricao&cod_hor=" + cod_hor + "&sta=" + status, {

    },
    function (data, status) {
        $(id_btn_buffering).removeClass('botao_buffering');

        if (data == "0") {
            data = "Não há mais vagas disponíveis para este curso.";
        } else {

            fnc_retorno();
            //inscrito
            //alterar_status(cod_hor, 'inscrito');
            // $(id_btn_inscrito).val('CANCELAR INSCRIÇÃO');
            //  var fnc_on_click = function () { mostra_balao('bal_' + cod_hor, cod_hor, 'Tem certeza que deseja cancelar sua inscrição?', 'cancelar'); };
            //  document.getElementById((id_btn_inscrito + "").toString().replace("#", '')).onclick = fnc_on_click;
        }
        //  mostra_balao('balao_' + cod_hor, cod_hor, data, "informar", 5000);
    });
}


function avaliacao_preencher(id_base,ava,fixa) {

    if (!hasValue(ava)) return false;

   // alert(window.avaliacao_atual);
   // $(id_base + '_1').removeClass('avaliacao_on');
    $(id_base + '_2').removeClass('avaliacao_on');
    $(id_base + '_3').removeClass('avaliacao_on');
    $(id_base + '_4').removeClass('avaliacao_on');
    $(id_base + '_5').removeClass('avaliacao_on');

    if (fixa) {
        if (ava >= 1) $(id_base + '_1').addClass('avaliacao_on');
        if (ava >= 2) $(id_base + '_2').addClass('avaliacao_on');
        if (ava >= 3) $(id_base + '_3').addClass('avaliacao_on');
        if (ava >= 4) $(id_base + '_4').addClass('avaliacao_on');
        if (ava >= 5) $(id_base + '_5').addClass('avaliacao_on');
        window.avaliacao_atual = ava;
    }
    else {
 if (ava > 1)  $(id_base + '_1').addClass('avaliacao_on');
  if (ava > 2) $(id_base + '_2').addClass('avaliacao_on');
  if (ava > 3) $(id_base + '_3').addClass('avaliacao_on');
  if (ava > 4) $(id_base + '_4').addClass('avaliacao_on');
  if (ava > 5) $(id_base + '_5').addClass('avaliacao_on');
    }


}


function enviar_avaliacao(avalicao_score,tipo,cod_aux,descricao,depoimento,comentario_publico,funcao_retorno) {

    if (!hasValue(avalicao_score)) return false;

    //   alert(comentario_publico);



    $.post("/inserir_dado?tipo_dado=avaliacao_geral",
        {
            ava_1: avalicao_score,
            ava_2: 0,
            ava_3: 0,
            ava_4: 0,
            ava_5: 0,
            tip: tipo,
            cod_aux: cod_aux,
            des: descricao,
            com_pbl: comentario_publico,
            dep: depoimento,
            obs: ''
        },
            function (data, status) {
                if (hasValue(funcao_retorno)) {
                    var fnc_preenche_campos = new Function(funcao_retorno);
                    fnc_preenche_campos();
                }
            });
}


function retorna_nome_pagina_atual() {

    var url = location.href;
    var file_with_parameters = url.substr(url.lastIndexOf('/') + 1);
    var file = file_with_parameters.substr(0, file_with_parameters.lastIndexOf('?'));

    return file;
}

function inc_sha(dados_inc) {



    if (!hasValue(dados_inc)) return false;



    $.post("/inserir_dado?tipo_dado=inc_sha",
        {
            dados_inc: dados_inc
        },
            function (data, status) {

            });
}



function gera_menu_compartilhar(id_div, url, texto_de_compartilhamento_fb, texto_de_compartilhamento_tw, texto_de_compartilhamento_lk, dados_inc, tipo_conteudo_alternativo, seta_para_baixo) {
    // alert(tipo_conteudo_alternativo);

    if (tipo_conteudo_alternativo == 'profile_privado') {

        var innerHtml = '<div id="seta" class="triangulo_para_cima_branco" style="  margin-left: 380px; margin-top: -10px;    z-index: 99999 !important"></div>' +
                  ' <br/> <br/>   <br/> <span style="color: black; font-family: klavika_bdbold; font-size: 14px;">PARA PODER COMPARTILHAR ESTE PROFILE É NECESSÁRIO TORNÁ-LO PÚBLICO.</span>' +
                  '<br/>';



    }
    else if (tipo_conteudo_alternativo == 'carteira_privado') {
        var innerHtml = '<div id="seta" class="triangulo_para_cima_branco" style="  margin-left: 380px; margin-top: -10px;    z-index: 99999 !important"></div>' +
                     ' <br/> <br/>   <br/> <span style="color: black; font-family: klavika_bdbold; font-size: 14px;">PARA PODER COMPARTILHAR ESTA CARTEIRA É NECESSÁRIO TORNÁ-LA PÚBLICA.</span>' +
                     '<br/>';
    }

    else {





    url = 'https://www.clubefii.com.br/' + url
    if (hasValue(texto_de_compartilhamento_tw)) texto_de_compartilhamento_tw = texto_de_compartilhamento_tw + ' '; else texto_de_compartilhamento_tw = ''
    if (hasValue(texto_de_compartilhamento_lk)) texto_de_compartilhamento_lk = texto_de_compartilhamento_lk + ' '; else texto_de_compartilhamento_lk = ''
    var innerHtml =
        (seta_para_baixo
            ? '<div id="seta" class="triangulo_para_baixo_branco" style="position:absolute;  margin-left: 380px; margin-top: 168px;    z-index: 99999 !important"></div>'
            : '<div id="seta" class="triangulo_para_cima_branco" style="  margin-left: 380px; margin-top: -10px;    z-index: 99999 !important"></div>'
        )
        +
                    ' <br/> <span style="color: black; font-family: klavika_bdbold; font-size: 14px;"> COMPARTILHAR</span>' +
                    '<br/>' +
                    '<a onclick="inc_sha(\'' + dados_inc + '\')" href="https://www.facebook.com/sharer/sharer.php?u=' + url + '" target="_blank">' +
                    '        <input type="button"  class="fsSubmitButton" value="FACEBOOK" style="text-align:center; font-size:15px !important; width:115px; height:30px; margin-top:5px; padding-right: 30px; background-image: url(\'//cdn.clubefii.com.br/img/old/ico_sha_fb.png\'); background-position:right; background-repeat: no-repeat; background-size: 30px; "/>' +
                    '</a>' +
                    '<a onclick="inc_sha(\'' + dados_inc + '\')" class="twitter-share-button" href="https://twitter.com/intent/tweet?text=' + texto_de_compartilhamento_tw + url + '" target="_blank">' +
                    '    <input type="button"  class="fsSubmitButton" value="TWITTER" style="text-align:center; margin-left: 5px; font-size:15px !important; width:115px; height:30px; margin-top:5px; padding-right: 30px; background-image: url(\'//cdn.clubefii.com.br/img/old/ico_sha_tw.png\'); background-position:right; background-repeat: no-repeat; background-size: 30px; "/>' +
                    '</a>' +
                    '     <a onclick="inc_sha(\'' + dados_inc + '\')" class="linkedin-share-button" href="https://www.linkedin.com/cws/share?url=' + texto_de_compartilhamento_lk + url + '" target="_blank">' +
                    '             <input type="button"  class="fsSubmitButton" value="LINKEDIN" style="text-align:center; margin-left: 5px; font-size:15px !important; width:115px; height:30px; margin-top:5px; padding-right: 30px; background-image: url(\'//cdn.clubefii.com.br/img/old/ico_sha_lk.png\'); background-position:right; background-repeat: no-repeat; background-size: 30px; "/>' +
                      '</a>' +
                   '     <br/><br/>' +
                    '     <span style="color: black; font-family: klavika_bdbold;  font-size: 14px;">COPIAR LINK</span>' +
                    '    <input  value="' + url + '" type="text" readonly="readonly" onclick=" $(this).select();" onmouseup="this.onmouseup = null; return false;" class="text_padrao" style="width: 319px;  margin-top: 5px  !important; padding-left: 3px !important; padding-right: 35px !important;  color: black; background: url(\'//cdn.clubefii.com.br/img/old/ico_pro_link2.png\')  no-repeat #f1f1f1 right; background-size: 30px;"/>';
}
    $(id_div).html(innerHtml);
    if ($(id_div).is(':visible') == true) { $(id_div).hide(); } else { $(id_div).show(); }
}

function abrir_popup_personalizado_v2(mensagem) {
    $('#popup_generico_texto').html(mensagem);

    popup('popUpDiv_generico');
}

function abrir_popup_generico_v2(titulo, mensagem, op_botao_ok, op_altura,op_largura,op_funcao_botao) {

  //  if (!hasValue(op_altura)) op_altura = '200';
    if (!hasValue(op_largura)) op_largura = '600';

    if (!hasValue(op_botao_ok)) op_botao_ok = 'OK';


  $('#popup_generico_titulo_v2').html(titulo);

  $('#popup_generico_texto_v2').html(mensagem);



  $('#btn_pop_ok_v2').val(op_botao_ok);


     $('#popUpDiv_generico_v2').fadeIn(500);


  if (hasValue(op_altura)) document.getElementById("popUpDiv_generico_v2").style.height = op_altura + 'px';
  if (hasValue(op_largura)) document.getElementById("popUpDiv_generico_v2").style.width = op_largura + 'px';



    apaga_luz_v2();






//    alert(-(document.getElementById("popUpDiv_generico_v2").offsetHeight / 2) + 'px');

    document.getElementById("popUpDiv_generico_v2").style.marginTop = -(document.getElementById("popUpDiv_generico_v2").offsetHeight / 2) + 'px';
    document.getElementById("popUpDiv_generico_v2").style.marginLeft = -(document.getElementById("popUpDiv_generico_v2").offsetWidth / 2) + 'px';

   //width: 750px; height: 445px; margin-left: -375px; margin-top: -220px;--%>


}

function abrir_popup_generico_ok(mensagem) {
    $('#popup_generico_texto').html(mensagem);

    popup('popUpDiv_generico');
}

function atualiza_visibilidade_num_itens_carrinho(forcar_esconder) {
    //alert($('#num_ite_car').text());




    if ($('#num_ite_car').text() == 0 || forcar_esconder == true) { $('#cir_carrinho').hide(); } else { $('#cir_carrinho').show(); }

    if ($('#num_ite_car').text() > 9) { $('#cir_carrinho').removeClass('circulo_carrinho_espaco_1_digito').addClass('circulo_carrinho_espaco_2_digitos'); }
    else { $('#cir_carrinho').removeClass('circulo_carrinho_espaco_2_digitos').addClass('circulo_carrinho_espaco_1_digito'); }


}

function carrega_tabela_personalizada(cod_ou_nom_profile, id_div, opcional_variavel_adicional, opcional_variavel_adicional2, opcional_variavel_adicional3, op_mostra_num_registros,op_tabela_clicavel) {

  //  alert(op_mostra_num_registros);

    $(id_div).addClass('adiciona_opacidade');

   // alert(cod_ou_nom_profile);


    if (!hasValue(op_mostra_num_registros)) op_mostra_num_registros = true;

    if (!hasValue(op_tabela_clicavel)) op_tabela_clicavel = true;
    //alert(op_clicavel)
    $.post("/tabela_personalizada",
        {
            op_clicavel: op_tabela_clicavel,
            cod_ou_nom: cod_ou_nom_profile,
            vars_opcional: opcional_variavel_adicional,
            vars_opcional2: opcional_variavel_adicional2,
            vars_opcional3: opcional_variavel_adicional3,
            mostra_num_registros: op_mostra_num_registros
        },

        function (data, status) {
            $(id_div).removeClass('adiciona_opacidade');
            $(id_div).html(data);
        }
    );

    return false;
}


function adiciona_item_carrinho(tip, cod_pro, des_pro, qtd, val, id_btn, op_url_alternativa,op_reload_apos_add) {

    try { val = val.replace('.',','); }
    catch(ex) {

    }


   // alert(tip + cod_pro + des_pro + val);
    if (!hasValue(op_reload_apos_add)) op_reload_apos_add = false;
    if (!hasValue(op_url_alternativa)) op_url_alternativa = '/carrinho_add_item'; //url padrao

   //cod_pro = codigo_produto|descricao

    $(id_btn).removeClass('botao_efetuar_addcart');
    $(id_btn).addClass('botao_buffering');
    $(id_btn).val(' ');
    // alert(tip + ' -- ' + des_pro + ' -- ' + qtd + ' -- ' + val);

    $.ajax({

        data: {
            tip: tip,
            cod_pro: cod_pro,
            des_pro: des_pro,
            qtd: qtd,
            val: val,
        },
        type: "post",
        url: op_url_alternativa,
        async: true,
        success: function (data) {

            $("#num_ite_car").text(data.split('|')[0]);


            $(id_btn).removeClass('botao_buffering');
            $(id_btn).addClass('botao_efetuar_addcart');
            $(id_btn).val('ITEM ADICIONADO');

            atualiza_visibilidade_num_itens_carrinho();

            if (op_reload_apos_add) window.location.href = 'finalizar_pedido';

            return data;



        }
    });



}

function remover_item_carrinho(id, tipo_e_codigo_produto, valor, op_id_item_tela_finalizar_pedido,op_url_alternativa) {
   // alert(op_url_alternativa);
    if (!hasValue(op_url_alternativa)) op_url_alternativa = 'carrinho.aspx?remover_item='; //padrao clubefii

    //alert(id + ' , ' + tipo_e_codigo_produto + ' , ' + valor + ' , ' + op_id_item_tela_finalizar_pedido + ' , ' + op_url_alternativa);

   // alert(op_url_alternativa);
    $.ajax({

        data: {
        },
        type: "post",
        url: op_url_alternativa + tipo_e_codigo_produto,
        async: true,
        success: function (data) {
            $("#num_ite_car").text(data.split('|')[0]);

            atualiza_visibilidade_num_itens_carrinho();

            if (data.split('|')[0] == 0) {
                //alert($("#pedido_total_valor").text().replace(',', '.'));
                try {
                    $("#pedido_tit_itens_pagina").text('NÃO HÁ NENHUM ITEM NO SEU CARRINHO');
                  //  alert($("#pedido_total_valor").text());
                    }
                catch (err) {

                }


            }

            try {
                $("#pedido_total_valor").text(($("#pedido_total_valor").text().replace(',', '.') - valor).toFixed(2).replace('.', ','));
                if ($('#pedido_total_valor').text() == '0,00') { $('#pedido_total_botoes').hide() } else { $('#pedido_total_botoes').show() }

                $(op_id_item_tela_finalizar_pedido).slideUp(500);
               // alert(op_id_item_tela_finalizar_pedido);
            } catch (err) { }




            try {
                $('#pedido_item_' + (parseInt(id) + 1)).hide();
                $("#cart_total_valor_pedido").text('R$ ' + ($("#cart_total_valor_pedido").text().split(' ')[1].replace(',', '.') - valor).toFixed(2).replace('.', ','));
            } catch (err) { }
        }
    });

}

function carrega_carrinho(id, op_url_alternativa) {


    if (!hasValue(op_url_alternativa)) op_url_alternativa = 'carrinho'; //url padrao clubefii


    if ($('#itens_carrinho').is(":visible") == false) { $('#itens_carrinho').show(); } else { return false; }

    $(id).html('');
$('#conteudo_carrinho_buffering').show();

    $('#menu_inteiro_alertas').hide();
    $('#container_fiis_seguidos_e_menu').hide();

   // $('#itens_carrinho').html('<img src="//cdn.clubefii.com.br/img/old/buffering_mini.gif" style="margin-top: 10px;" / >');

    //return false;

    $(id).load(op_url_alternativa, function (responseTxt, statusTxt, xhr) {
        if (statusTxt == "success") {
            $('#conteudo_carrinho_buffering').hide();
            atualiza_visibilidade_num_itens_carrinho();
        }

        if (statusTxt == "error") {

        }

    });


}

function pega_toda_query_url() {
    return window.location.href.slice(window.location.href.indexOf('?') + 1, window.location.href.length);
}

function converteFloatMoeda(valor) {
    var inteiro = null, decimal = null, c = null, j = null;
    var aux = new Array();
    valor = "" + valor;
    c = valor.indexOf(".", 0);
    //encontrou o ponto na string
    if (c > 0) {
        //separa as partes em inteiro e decimal
        inteiro = valor.substring(0, c);
        decimal = valor.substring(c + 1, valor.length);
    } else {
        inteiro = valor;
    }

    //pega a parte inteiro de 3 em 3 partes
    for (j = inteiro.length, c = 0; j > 0; j -= 3, c++) {
        aux[c] = inteiro.substring(j - 3, j);
    }

    //percorre a string acrescentando os pontos
    inteiro = "";
    for (c = aux.length - 1; c >= 0; c--) {
        inteiro += aux[c] + '.';
    }
    //retirando o ultimo ponto e finalizando a parte inteiro

    inteiro = inteiro.substring(0, inteiro.length - 1);

    decimal = parseInt(decimal);
    if (isNaN(decimal)) {
        decimal = "00";
    } else {
        decimal = "" + decimal;
        if (decimal.length === 1) {
            decimal = decimal + "0";
        }
    }


    valor = "R$ " + inteiro + "," + decimal;


    return valor;

}

function formatReal(num,op_incluir_prefixo) {

    if (!hasValue(op_incluir_prefixo)) op_incluir_prefixo = true;

        x = 0;

        if(num<0) {
            num = Math.abs(num);
            x = 1;
        }
        if(isNaN(num)) num = "0";
        cents = Math.floor((num*100+0.5)%100);

        num = Math.floor((num*100+0.5)/100).toString();

        if(cents < 10) cents = "0" + cents;
        for (var i = 0; i < Math.floor((num.length-(1+i))/3); i++)
            num = num.substring(0,num.length-(4*i+3))+'.'
                  +num.substring(num.length-(4*i+3));
        ret = num + ',' + cents;

        if (x == 1) ret = ' - ' + ret; return (op_incluir_prefixo ? 'R$ ' : "") + ret;

    }


function left(str, n)
{
    if (n <= 0)
        return "";
    else if (n > String(str).length)
        return str
    else
        return String(str).substring(0,n);
}

function right(str, n)
{
    if (n <= 0)
        return "";
    else if (n > String(str).length)
        return str;
    else
        var iLen = String(str).length;
    return String(str).substring(iLen, iLen - n);
}


function atualiza_alertas () {

    $.ajax({

        type: "GET",
        url: "/fundos_listagem.aspx?termo=" + termo + "&ordenar=cod&compacto=true",
        async: true,
        success: function (data) {

            //$('#loadingmessage').hide();
            //$('#carrega').hide();

            remote = data;



            //document.getElementById("busca_resultado").innerHTML = remote;
            $("#busca_resultado").html(remote);

            //$('#busca_resultado').attr("style", "display: normal");

            $('#busca_resultado').slideDown(500);

            $('#txt_bus').removeClass('texto_buffering');
            $('#txt_bus').removeClass('texto_buffering_mini');

            //  $('.texto_busca').attr("style", "background-image: none");



        }
    });


    return remote;

}

//funcao j query para pegar query string: uso $.QueryString['parametro']
(function ($) {
    $.QueryString = (function (a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i) {
            var p = a[i].split('=');
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'))
})(jQuery);


function gettok(s, n, c) {
    var c = String.fromCharCode(c), sa = s.split(c);
    if (!/-/.test(n)) {
        n = (n - 1);
        return ((sa[n]) ? sa[n] : NaN);
    } else {
        n = n.split('-'), o = new Array();
        var x = ((n[1]) ? n[1] : s.length)
        for (var i = (n[0] - 1) ; i < x; i++) o.push(sa[i]);
        return ((o.length > 0) ? o.join(c) : NaN);
    }
}


function adiciona_texto_a_textbox(id,texto) {

    $('#' + id).val($('#' + id).val() + texto);

}

function cotacao_fundo(codigo_neg,id_div_resultado) {

//$('#resultado').html('carregando');

    url = 'http://www.bmfbovespa.com.br/Pregao-Online/ExecutaAcaoCarregarDadosPapeis.asp?CodDado=' + codigo_neg




// if it is an external URI
if (url.match('^http')) {

    // call YQL
    $.getJSON("http://query.yahooapis.com/v1/public/yql?" +
              "q=select%20*%20from%20html%20where%20url%3D%22" +
              encodeURIComponent(url) +
              "%22&format=xml'&callback=?",
      // this function gets the data from the successful
      // JSON-P call


      function (data) {


        //  alert(data.results[0]);
         // $('#' + codigo_neg).text('#' + id_div_resultado);

          // if there is data, filter it and render it out
          if (data.results[0]) {

              data = data.results[0]

            // var data = filterData(data.results[0]);

              //  $('#resultado').html(data);

    // data = data.replace('|','£')




              cotacao_abertura = data.split('|');

           //   alert(cotacao_abertura[0].split('=')[1] + cotacao_abertura[0].split('=')[2]);



             // alert('oscilacao : ' + cotacao_abertura[0].split('=')[2].split('@')[2]);


              result = data.split('|');

              //alert('ultima atualizacao horario: ' + result[result.length - 2].split('@')[0]);

              //alert('ultima atualizacao cotacao: ' + result[result.length - 2].split('@')[1]);

              //alert('ultima atualizacao variacao: ' + result[result.length - 2].split('@')[2]);

              var resultado_completo = new Array(
                  cotacao_abertura[0].split('=')[1].split('&')[0], // 0- data do pregão
                  cotacao_abertura[0].split('=')[2].split('@')[0], //1- horário
                  cotacao_abertura[0].split('=')[2].split('@')[1], //2-cotação inicial
                  cotacao_abertura[0].split('=')[2].split('@')[2], //3- oscilacao inicial
                  result[result.length - 2].split('@')[0], //4- ultimo horario
                  result[result.length - 2].split('@')[1], //5- ultima cotacao
                  result[result.length - 2].split('@')[2] //6- ultima oscilacao

                  );




             // alert(result);

           // alert(id_div_resultado + result[result.length - 1]);

              //   $('#' + id_div_resultado).text(result[0] + ' resultado: ' + result[result.length - 2]);

              $('#' + id_div_resultado).text('resultado: ' + resultado_completo);

              return resultado_completo;

              //container.html(data);
              // otherwise tell the world that something went wrong
          } else {
              var errormsg = '<p>Error: cant load the page.</p>';
             // alert(errormsg);
              // container.html(errormsg);
          }
      }
    );
    // if it is not an external URI, use Ajax load()
} else {

   // alert('data2 ' + data);
    //$('#target').load(url);
}
//}
// filter out some nasties

function filterData(data) {
    data = data.replace(/<?\/body[^>]*>/g, '');
    data = data.replace(/[\r|\n]+/g, '');
    data = data.replace(/<--[\S\s]*?-->/g, '');
    data = data.replace(/<noscript[^>]*>[\S\s]*?<\/noscript>/g, '');
    data = data.replace(/<script[^>]*>[\S\s]*?<\/script>/g, '');
    data = data.replace(/<script.*\/>/, '');
    return data;
}

}



function validateEmail($email) {

    if ($email.length == 0) { return false; }


    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;



    if (!emailReg.test($email)) {
        return false;
    } else {
        return true;
    }
}







 var timeoutID;

function setup_idle() {
    this.addEventListener("mousemove", resetTimer, false);
    this.addEventListener("mousedown", resetTimer, false);
    this.addEventListener("keypress", resetTimer, false);
    this.addEventListener("DOMMouseScroll", resetTimer, false);
    this.addEventListener("mousewheel", resetTimer, false);
    this.addEventListener("touchmove", resetTimer, false);
    this.addEventListener("MSPointerMove", resetTimer, false);

    startTimer();
}
setup_idle();




function startTimer() {
    // wait 2 seconds before calling goInactive
    timeoutID = window.setTimeout(goInactive, 60000); //configuracao de intervalo dos alertas
}

function resetTimer(e) {
    window.clearTimeout(timeoutID);

    goActive();
}

function goInactive() {
    window.usuario_esta_ativo = false;
}

function goActive() {

    if (window.usuario_esta_ativo == false) {
        mostra_esconde_alertas(true);
    }

    window.usuario_esta_ativo = true;

    startTimer();
}


function libera_inclusao_dados() {

    $('#balao').addClass('balao_para_direita_ativado');
    $('#balao').text('Clique aqui para continuar');
}

function prepara_data() {



    $(function () {
        $(".data_picker").datepicker({
            dateFormat: 'dd/mm/yy',
            dayNames: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
            dayNamesMin: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S', 'D'],
            dayNamesShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
            monthNames: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            monthNamesShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        });
    });

}

function prepara_data_formato_mes_ano() {



    $(function () {
        $(".data_picker_mes_ano").datepicker({
            dateFormat: 'mm/yy',
            dayNames: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
            dayNamesMin: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S', 'D'],
            dayNamesShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
            monthNames: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            monthNamesShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        });
    });

}

function prepara_data_formato_data_hora() {



    $(function () {
        $(".data_picker_data_hora").datepicker({
            dateFormat: 'dd/mm/yy 00:00',
            dayNames: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
            dayNamesMin: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S', 'D'],
            dayNamesShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
            monthNames: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            monthNamesShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        });
    });

}

function formatar_moeda_real(campo, separador_milhar, separador_decimal, tecla) {

  //para textbox

    var sep = 0;
    var key = '';
    var i = j = 0;
    var len = len2 = 0;
    var strCheck = '0123456789';
    var aux = aux2 = '';
    var whichCode = (window.Event) ? tecla.which : tecla.keyCode;

    if (whichCode == 13) return true; // Tecla Enter
    if (whichCode == 8) return true; // Tecla Delete
    key = String.fromCharCode(whichCode); // Pegando o valor digitado
    if (strCheck.indexOf(key) == -1) return false; // Valor inválido (não inteiro)
    len = campo.value.length;
    for (i = 0; i < len; i++)
        if ((campo.value.charAt(i) != '0') && (campo.value.charAt(i) != separador_decimal)) break;
    aux = '';
    for (; i < len; i++)
        if (strCheck.indexOf(campo.value.charAt(i)) != -1) aux += campo.value.charAt(i);
    aux += key;
    len = aux.length;
    if (len == 0) campo.value = '';
    if (len == 1) campo.value = '0' + separador_decimal + '0' + aux;
    if (len == 2) campo.value = '0' + separador_decimal + aux;

    if (len > 2) {
        aux2 = '';

        for (j = 0, i = len - 3; i >= 0; i--) {
            if (j == 3) {
                aux2 += separador_milhar;
                j = 0;
            }
            aux2 += aux.charAt(i);
            j++;
        }

        campo.value = '';
        len2 = aux2.length;
        for (i = len2 - 1; i >= 0; i--)
            campo.value += aux2.charAt(i);
        campo.value += separador_decimal + aux.substr(len - 2, len);
    }

    return false;
}



function retorna_valor_text_box(txt_box) { return $(txt_box).val(); }



function setSelectByValue(eID, val) { //Loop through sequentially//

    var ele = document.getElementById(eID);
    for (var ii = 0; ii < ele.length; ii++)
        if (ele.options[ii].value == val) { //Found!
            ele.options[ii].selected = true;
            return true;
        }
    return false;
}

function setSelectByText(eID, text) { //Loop through sequentially//

    //seleciona item da select tag por texto. sintaxe: setSelectByText('id_sem_tralha','texto')
    var ele = document.getElementById(eID);
    for (var ii = 0; ii < ele.length; ii++)
        if (ele.options[ii].text == text) { //Found!
            ele.options[ii].selected = true;
            return true;
        }
    return false;
}

function carrega_pop_texto(arquivo) {

    apaga_luz_v2();

    $('#pop_textos').html('');
    $('#pop_textos').show(500);

    $('#pop_textos').addClass('popup_textos_buffering')

    $("#pop_textos").load(arquivo, function (responseTxt, statusTxt, xhr) {
        if (statusTxt == "success") { $('#pop_textos').removeClass('popup_textos_buffering'); }

        if (statusTxt == "error") { }

    });


}



function abre_popup_obrigado(janela) {



    $.ajax({

        data: {
            janela: janela
        },
        type: "post",
        url: "/colaborar_popup_obrigado",
        success: function (data) {
            //   $('#balao').removeClass('balao_para_direita_buffering');

            $("#popup").html(data);


            //  $("#col_txt_tip").val(tip);

            //   $('#corpo_inteiro').addClass('adiciona_transparencia');


            $('#popup').show();

            // document.getElementById("popup").style.height = "370";

            $('#popup').removeClass('popup_colaborar_altura_contratos')

            $('#popup').removeClass('popup_colaborar_altura_proventos').addClass('popup_colaborar_obrigado');

            $('.pop_light').allofthelights({ 'z_index': '10000', 'opacity': '0.7' });
        }
    });

}



function adiciona_buffering_textbox(id, mini) {

    if (mini == true) { $(id).addClass('texto_buffering_mini'); } else { $(id).addClass('texto_buffering'); }


}

function remove_buffering_textbox(id) {
    $(id).removeClass('texto_buffering_mini');
    $(id).removeClass('texto_buffering');
}

function verifica_buffering_textbox(id) {


    if ($(id).hasClass('texto_buffering_mini') || ($(id).hasClass('texto_buffering'))) { return true; } else { return false; }
}

function tooltip_adiciona(div_id,span_id,texto,timer_desaparecer,op_com_html) {

    if (!hasValue(op_com_html)) op_com_html = false;

    $(div_id).addClass('tooltips_mostra');

    if (op_com_html) { $(span_id).html(texto); }
    else { $(span_id).text(texto); }




    if (timer_desaparecer > 0) {

        myVar = setTimeout(function () { tooltip_remove(div_id, span_id) }, timer_desaparecer);

    }

}
function tooltip_remove(div_id, span_id) {
    $(div_id).removeClass('tooltips_mostra');
    $(span_id).text('');

}


function Linkify(inputText) {


    //URLs starting with http://, https://, or ftp://
    var replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    var replacedText = inputText.replace(replacePattern1, '<a href="$1" target="_blank">$1</a>');

    //URLs starting with www. (without // before it, or it'd re-link the ones done above)
    var replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    var replacedText = replacedText.replace(replacePattern2, '$1<a href="http://$2" target="_blank">$2</a>');

    //Change email addresses to mailto:: links
    var replacePattern3 = /(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})/gim;
    var replacedText = replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');

    return replacedText
}

function ValidUrl(str) {
    //verifica se string é link
    var pattern = new RegExp('^(https?:\\/\\/)?' + // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
    '(\\#[-a-z\\d_]*)?$', 'i'); // fragment locator
    if (!pattern.test(str)) {
        return false;
    } else {
        return true;
    }
}

function isdate(data) {

    var dia = data.substring(0, 2)
    var mes = data.substring(3, 5)
    var ano = data.substring(6, 10)

    //Criando um objeto Date usando os valores ano, mes e dia.
    var novaData = new Date(ano, (mes - 1), dia);

    var mesmoDia = parseInt(dia, 10) == parseInt(novaData.getDate());
    var mesmoMes = parseInt(mes, 10) == parseInt(novaData.getMonth()) + 1;
    var mesmoAno = parseInt(ano) == parseInt(novaData.getFullYear());

    if (!((mesmoDia) && (mesmoMes) && (mesmoAno))) {
        //alert('Data informada é inválida!');
        //obj.focus();
        return false;
    }
    return true;
}

function isEmpty(value) {
    return (typeof value === "undefined" || value === null || value.length === 0);
}

function linkify_text(text) {
    if (text) {
        text = text.replace(
            /((https?\:\/\/)|(www\.))(\S+)(\w{2,4})(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/gi,
            function (url) {
                var full_url = url;
                if (!full_url.match('^https?:\/\/')) {
                    full_url = 'http://' + full_url;
                }
                return '<a href="' + full_url + '">' + url + '</a>';
            }
        );
    }
    return text;
}


var isMobile = {
    Android: function () {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function () {
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function () {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function () {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function () {
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function () {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
    }
};


function isIE(userAgent) {
    userAgent = userAgent || navigator.userAgent;
    return navigator.appVersion.indexOf('Edge') > -1 || userAgent.indexOf("MSIE ") > -1 || userAgent.indexOf("Trident/") > -1;
}

function abre_popup(id_botao_buffering,nome_arquivo_janela_pop) {

    //   alert($('#col_txt_des_tit').val());


    txt_btn = $(id_botao_buffering).val();

    $(id_botao_buffering).addClass('botao_buffering');
    $(id_botao_buffering).val(' ');



    $.ajax({

        type: "post",
        url: nome_arquivo_janela_pop,
        success: function (data) {


           $("#popup").html(data);




            $(id_botao_buffering).removeClass('botao_buffering');
            $(id_botao_buffering).val(txt_btn);

            $('#popup').show();

            $('#popup').removeClass('popup_colaborar_altura_proventos').addClass('popup_colaborar_altura_contratos');

            $('.pop_light').allofthelights({ 'z_index': '10000', 'opacity': '0.7', });

        }
    });

}

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

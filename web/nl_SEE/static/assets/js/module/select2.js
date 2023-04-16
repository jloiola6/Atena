// Script para inicializar o componente select2

(() => {
    const $select2 =  $('[data-selecao2]').select2({
        language: {
            noResults: function () {
              return "Nenhum resultado encontrado";
            }
          }
    })
    const $select2Container = $('.select2-container')

    $select2Container.removeAttr('style')
})

()
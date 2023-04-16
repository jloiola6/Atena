(() => {

    // Inspecionar as tabelas presentes na página
        const tabelas = document.querySelectorAll('[data-grafico]')
    
        // Extratir os labels e dados
    
        if(tabelas)
            tabelas.forEach((tabela) => {
                const labels = [...tabela.querySelectorAll('th')].map(th => th.textContent)
                const dados = [...tabela.querySelectorAll('td')].map(td => td.textContent)
                
                // INICIANDO A CONSTRUÇÃO DOS GRÁFICOS
                const tipo = tabela.dataset.grafico
    
                // Função para inicializar o tipo de gráfico de acordo com o tipo passado pelo atributo da tabela
                const getType = () => {
                    switch (tipo) {
                        case 'linha':
                            return 'line'
                        case 'barra', 'barra-horizontal':
                            return 'bar'
                        case 'donut':
                            return 'doughnut'
                    }
    
                    return 'bar'
                }
    
                const getOrientacao = () => {
                    return tipo == 'barra-horizontal' ? 'y' : 'x'
                }
    
                // SETUP
                
                const cores = ['#104183', '#2067C6', '#4883F8', '#8EBEFF']
    
                const data = {
                    labels: labels,
                    datasets: [{
                        label: '',
                        backgroundColor: cores,
                        data: dados,
                        hoverOffset: 8,
                    }]  
                }
    
                // CONFIG
                
                const config = {
                    type: getType(),
                    data: data,
                    options: {
                        layout: {
                            padding: 8
                        },
    
                        plugins: {
                            legend: {
                                labels: {
                                    // This more specific font property overrides the global property
                                    font: {
                                        family: "'Hurme Geometric Sans 4', sans-serif",
                                        size: 16
                                    }
                                }
                            }
                        },
    
                        indexAxis: getOrientacao()
                    }
                } 
                
                // RENDER
    
                const canvas = document.createElement('canvas')
                
                const grafico = new Chart(canvas, config)
    
                tabela.parentElement.appendChild(canvas)
                tabela.remove()
            })
    })
    
    ()
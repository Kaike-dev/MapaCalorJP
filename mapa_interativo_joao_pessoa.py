import folium
import pandas as pd
import geopandas as gpd
import os 


dados = {
    "Bairro": ["Manaíra", "Tambaú", "Bessa", "Centro", "Jaguaribe"],
    "Secretaria": ["Saúde", "Educação", "Infraestrutura", "Segurança", "Cultura"],
    "Quantidade": [200, 120, 80, 60, 40]
}
df = pd.DataFrame(dados)
print("--- Dados Iniciais ---")
print(df)
print("-" * 25)



geojson_path = "joao_pessoa_bairros.geojson"


if not os.path.exists(geojson_path):
    print(f"ERRO: Arquivo '{geojson_path}' não encontrado.")
    print("Por favor, certifique-se de que o arquivo está na mesma pasta que este script.")
else:
    
    gdf = gpd.read_file(geojson_path)
    print(f"'{geojson_path}' carregado com sucesso.")
    
    
    mapa_gdf = gdf.merge(df, left_on="nome", right_on="Bairro", how="left")

   
    mapa_gdf['Quantidade'] = mapa_gdf['Quantidade'].fillna(0)
    mapa_gdf['Secretaria'] = mapa_gdf['Secretaria'].fillna('Sem dados')


    
    mapa = folium.Map(location=[-7.115, -34.864], zoom_start=12, tiles="CartoDB positron")


    
    choropleth = folium.Choropleth(
        geo_data=mapa_gdf,
        name="Demandas por Bairro",
        data=mapa_gdf,
        columns=["Bairro", "Quantidade"],
        
        key_on="feature.properties.nome",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name="Quantidade de Demandas",
        highlight=True 
    ).add_to(mapa)

    
    tooltip = folium.GeoJsonTooltip(
        fields=["nome", "Secretaria", "Quantidade"],
        aliases=["Bairro:", "Secretaria:", "Demandas:"],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
        sticky=True
    )
    choropleth.geojson.add_child(tooltip)
    

    
    folium.LayerControl().add_to(mapa)


    
    output_filename = "mapa_interativo_joao_pessoa.html"
    mapa.save(output_filename)
    print(f"\nMapa salvo com sucesso como '{output_filename}'")


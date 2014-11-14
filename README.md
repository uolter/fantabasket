

    import pandas as pd
    import numpy as np
    
    !ls

    1_get_players.py  2_get_profiles.py players.csv       profiles.csv
    1_teambuild.ipynb calendar.csv      players.csv.bak   profiles.csv.bak



    df = pd.read_csv('profiles.csv', sep=',')
    df.rename(columns={'+/-': 'Val'}, inplace=True)
    df.Val.fillna(0, inplace=True)
    # drop the Url -> is unuseful !!
    df.drop(['Url', 'Media'] , axis=1, inplace=True)
    
    df.head()




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Country</th>
      <th>PR</th>
      <th>PG</th>
      <th>SF</th>
      <th>PT</th>
      <th>MIN</th>
      <th>...</th>
      <th>Tot</th>
      <th>Dat</th>
      <th>Sub</th>
      <th>Per</th>
      <th>Rec</th>
      <th>Ass</th>
      <th>Lega</th>
      <th>OER</th>
      <th>Adp</th>
      <th>Val</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>  Archie Dominique</td>
      <td>     Upea Capo d'Orlando</td>
      <td>        Ala</td>
      <td> 27</td>
      <td>  USA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td> 16.2 </td>
      <td> 34.8 </td>
      <td>...</td>
      <td> 5.8 </td>
      <td> 0.0 </td>
      <td> 0.2 </td>
      <td> 3.0 </td>
      <td> 1.4 </td>
      <td> 2.4 </td>
      <td> 20.8 </td>
      <td> 1.011 </td>
      <td>  0.8 </td>
      <td> -2.6 </td>
    </tr>
    <tr>
      <th>1</th>
      <td>    Armwood Isaiah</td>
      <td> Dolomiti Energia Trento</td>
      <td> Ala/Centro</td>
      <td> 24</td>
      <td>  USA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  0.8 </td>
      <td>  4.4 </td>
      <td>...</td>
      <td> 0.2 </td>
      <td> 0.4 </td>
      <td> 0.0 </td>
      <td> 0.4 </td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> -0.4 </td>
      <td> 0.533 </td>
      <td> -0.4 </td>
      <td> -2.2 </td>
    </tr>
    <tr>
      <th>2</th>
      <td>      Banks Adrian</td>
      <td>        Sidigas Avellino</td>
      <td>    Guardia</td>
      <td> 29</td>
      <td>  USA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td> 12.6 </td>
      <td> 29.4 </td>
      <td>...</td>
      <td> 2.6 </td>
      <td> 0.0 </td>
      <td> 0.4 </td>
      <td> 3.8 </td>
      <td> 1.2 </td>
      <td> 2.4 </td>
      <td> 10.2 </td>
      <td> 0.827 </td>
      <td> -0.2 </td>
      <td>  6.2 </td>
    </tr>
    <tr>
      <th>3</th>
      <td> Bertocchi Edoardo</td>
      <td> Dolomiti Energia Trento</td>
      <td>     Centro</td>
      <td> 18</td>
      <td>  ITA</td>
      <td> NaN</td>
      <td> NaN</td>
      <td> NaN</td>
      <td>   NaN</td>
      <td>   NaN</td>
      <td>...</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>   NaN</td>
      <td>    NaN</td>
      <td>   NaN</td>
      <td>     0</td>
    </tr>
    <tr>
      <th>4</th>
      <td> Awudu Abass Abass</td>
      <td> Acqua Vitasnella CantÃ¹</td>
      <td>        Ala</td>
      <td> 22</td>
      <td>  ITA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  8.0 </td>
      <td> 19.2 </td>
      <td>...</td>
      <td> 1.8 </td>
      <td> 0.8 </td>
      <td> 0.0 </td>
      <td> 1.8 </td>
      <td> 0.8 </td>
      <td> 0.6 </td>
      <td>  7.6 </td>
      <td> 0.906 </td>
      <td> -0.4 </td>
      <td> -0.2 </td>
    </tr>
  </tbody>
</table>
<p>5 rows × 34 columns</p>
</div>




    def to_int(val):
        if isinstance(val, str):
            val = val.replace('\xc2\xa0', '').encode('utf-8')
            return np.float64(val)
        return val
    
    
    df.Val = df.Val.apply(to_int)
    
    def best_by_role(data, role, nret=5):
        player = data[data['Role'].isin(role)]
        
        # score must be integer
        return player.sort(['Val'], ascending=[False])[:nret]


    # compute price
    f = lambda x: x * 1000 if x >0 else x
    
    df['Price'] = df.Val.apply(f)
    # filter not used columns:
    
    df_small = df[["Name", "Team", "Role", "Age", "Val", "Price"]]


    best_by_role(df_small,['Ala', 'Ala/Centro'])




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Val</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>191</th>
      <td>         Moss David</td>
      <td> EA7 Emporio Armani Milano</td>
      <td>        Ala</td>
      <td> 31</td>
      <td> 9.3</td>
      <td> 9300</td>
    </tr>
    <tr>
      <th>103</th>
      <td>      Clark Cameron</td>
      <td>            Vanoli Cremona</td>
      <td>        Ala</td>
      <td> 23</td>
      <td> 9.0</td>
      <td> 9000</td>
    </tr>
    <tr>
      <th>52 </th>
      <td>         Ress Tomas</td>
      <td>       Umana Reyer Venezia</td>
      <td> Ala/Centro</td>
      <td> 34</td>
      <td> 8.2</td>
      <td> 8200</td>
    </tr>
    <tr>
      <th>207</th>
      <td>         Hanga Adam</td>
      <td>          Sidigas Avellino</td>
      <td>        Ala</td>
      <td> 25</td>
      <td> 7.8</td>
      <td> 7800</td>
    </tr>
    <tr>
      <th>138</th>
      <td> Lavrinovic Ksistof</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td> Ala/Centro</td>
      <td> 35</td>
      <td> 6.8</td>
      <td> 6800</td>
    </tr>
  </tbody>
</table>
</div>




    # Best Centro players
    best_by_role(df_small, ['Centro', 'Ala/Centro'])




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Val</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>113</th>
      <td>     Lawal Shane</td>
      <td> Banco di Sardegna Sassari</td>
      <td>     Centro</td>
      <td> 28</td>
      <td> 10.2</td>
      <td> 10200</td>
    </tr>
    <tr>
      <th>184</th>
      <td>      Mays James</td>
      <td>             Enel Brindisi</td>
      <td>     Centro</td>
      <td> 29</td>
      <td>  9.5</td>
      <td>  9500</td>
    </tr>
    <tr>
      <th>197</th>
      <td> Samuels Samardo</td>
      <td> EA7 Emporio Armani Milano</td>
      <td>     Centro</td>
      <td> 26</td>
      <td>  9.4</td>
      <td>  9400</td>
    </tr>
    <tr>
      <th>15 </th>
      <td>    Anosike O.D.</td>
      <td>          Sidigas Avellino</td>
      <td>     Centro</td>
      <td> 24</td>
      <td>  9.2</td>
      <td>  9200</td>
    </tr>
    <tr>
      <th>52 </th>
      <td>      Ress Tomas</td>
      <td>       Umana Reyer Venezia</td>
      <td> Ala/Centro</td>
      <td> 34</td>
      <td>  8.2</td>
      <td>  8200</td>
    </tr>
  </tbody>
</table>
</div>




    # Guardia Ala
    best_by_role(df_small, ['Guardia', 'Guardia/Ala'])




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Val</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>58 </th>
      <td>   Devecchi Giacomo</td>
      <td> Banco di Sardegna Sassari</td>
      <td> Guardia/Ala</td>
      <td> 30</td>
      <td> 10.3</td>
      <td> 10300</td>
    </tr>
    <tr>
      <th>221</th>
      <td>      Taylor Donell</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td>     Guardia</td>
      <td> 32</td>
      <td> 10.0</td>
      <td> 10000</td>
    </tr>
    <tr>
      <th>168</th>
      <td> Gentile Alessandro</td>
      <td> EA7 Emporio Armani Milano</td>
      <td>     Guardia</td>
      <td> 22</td>
      <td>  9.4</td>
      <td>  9400</td>
    </tr>
    <tr>
      <th>196</th>
      <td> Della Valle Amedeo</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td>     Guardia</td>
      <td> 21</td>
      <td>  7.2</td>
      <td>  7200</td>
    </tr>
    <tr>
      <th>18 </th>
      <td>      Denmon Marcus</td>
      <td>             Enel Brindisi</td>
      <td>     Guardia</td>
      <td> 25</td>
      <td>  6.6</td>
      <td>  6600</td>
    </tr>
  </tbody>
</table>
</div>




    # playmakers with score
    best_by_role(df_small, ['Playmaker', 'Play/Guardia'])




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Val</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>160</th>
      <td>     Vitali Luca</td>
      <td>             Vanoli Cremona</td>
      <td> Play/Guardia</td>
      <td> 28</td>
      <td> 11.7</td>
      <td> 11700</td>
    </tr>
    <tr>
      <th>91 </th>
      <td>  Moretti Davide</td>
      <td> Giorgio Tesi Group Pistoia</td>
      <td> Play/Guardia</td>
      <td> 16</td>
      <td> 10.0</td>
      <td> 10000</td>
    </tr>
    <tr>
      <th>80 </th>
      <td>    Dyson Jerome</td>
      <td>  Banco di Sardegna Sassari</td>
      <td> Play/Guardia</td>
      <td> 27</td>
      <td>  8.4</td>
      <td>  8400</td>
    </tr>
    <tr>
      <th>147</th>
      <td>     Ragland Joe</td>
      <td>  EA7 Emporio Armani Milano</td>
      <td> Play/Guardia</td>
      <td> 25</td>
      <td>  6.8</td>
      <td>  6800</td>
    </tr>
    <tr>
      <th>216</th>
      <td> Ruzzier Michele</td>
      <td>        Umana Reyer Venezia</td>
      <td>    Playmaker</td>
      <td> 22</td>
      <td>  5.4</td>
      <td>  5400</td>
    </tr>
  </tbody>
</table>
</div>




    # My Team
    
    my_team = df[df.Name.isin (
    ['Ruzzier Michele',
     'Moss David',
     'Devecchi Giacomo',
     'Lawal Shane',
     'Ress Tomas',
     'Vitali Michele',
     'Clark Cameron',
     'Harper Demonte',
     'Spera Andrea',
     'Gigli Angelo',
     'Imbrò Matteo',
     'Gaines Sundiata',
     'Cervi Riccardo'])]
    
    my_team




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Country</th>
      <th>PR</th>
      <th>PG</th>
      <th>SF</th>
      <th>PT</th>
      <th>MIN</th>
      <th>...</th>
      <th>Dat</th>
      <th>Sub</th>
      <th>Per</th>
      <th>Rec</th>
      <th>Ass</th>
      <th>Lega</th>
      <th>OER</th>
      <th>Adp</th>
      <th>Val</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>52 </th>
      <td>       Ress Tomas</td>
      <td>       Umana Reyer Venezia</td>
      <td>  Ala/Centro</td>
      <td> 34</td>
      <td>  ITA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  7.6 </td>
      <td> 24.8 </td>
      <td>...</td>
      <td> 0.6 </td>
      <td> 0.0 </td>
      <td> 0.8 </td>
      <td> 1.2 </td>
      <td> 0.8 </td>
      <td>  9.4 </td>
      <td> 0.999 </td>
      <td>  1.2 </td>
      <td>  8.2</td>
      <td>  8200</td>
    </tr>
    <tr>
      <th>58 </th>
      <td> Devecchi Giacomo</td>
      <td> Banco di Sardegna Sassari</td>
      <td> Guardia/Ala</td>
      <td> 30</td>
      <td>     </td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  4.0 </td>
      <td> 13.7 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.3 </td>
      <td> 1.0 </td>
      <td> 0.0 </td>
      <td>  6.7 </td>
      <td> 0.810 </td>
      <td>  0.7 </td>
      <td> 10.3</td>
      <td> 10300</td>
    </tr>
    <tr>
      <th>77 </th>
      <td>  Gaines Sundiata</td>
      <td>          Sidigas Avellino</td>
      <td>   Playmaker</td>
      <td> 28</td>
      <td>  USA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td> 10.0 </td>
      <td> 28.0 </td>
      <td>...</td>
      <td> 0.6 </td>
      <td> 0.4 </td>
      <td> 2.2 </td>
      <td> 1.2 </td>
      <td> 2.4 </td>
      <td>  6.8 </td>
      <td> 0.745 </td>
      <td>  1.4 </td>
      <td>  4.2</td>
      <td>  4200</td>
    </tr>
    <tr>
      <th>103</th>
      <td>    Clark Cameron</td>
      <td>            Vanoli Cremona</td>
      <td>         Ala</td>
      <td> 23</td>
      <td>  USA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td> 15.2 </td>
      <td> 30.8 </td>
      <td>...</td>
      <td> 0.2 </td>
      <td> 0.2 </td>
      <td> 1.0 </td>
      <td> 2.4 </td>
      <td> 0.8 </td>
      <td> 15.8 </td>
      <td> 1.035 </td>
      <td>  2.2 </td>
      <td>  9.0</td>
      <td>  9000</td>
    </tr>
    <tr>
      <th>113</th>
      <td>      Lawal Shane</td>
      <td> Banco di Sardegna Sassari</td>
      <td>      Centro</td>
      <td> 28</td>
      <td>  NIG</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  8.6 </td>
      <td> 26.4 </td>
      <td>...</td>
      <td> 2.0 </td>
      <td> 0.0 </td>
      <td> 2.0 </td>
      <td> 0.8 </td>
      <td> 1.0 </td>
      <td> 14.6 </td>
      <td> 0.906 </td>
      <td> -0.2 </td>
      <td> 10.2</td>
      <td> 10200</td>
    </tr>
    <tr>
      <th>120</th>
      <td>   Cervi Riccardo</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td>      Centro</td>
      <td> 23</td>
      <td>  ITA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  9.2 </td>
      <td> 26.6 </td>
      <td>...</td>
      <td> 1.8 </td>
      <td> 0.4 </td>
      <td> 1.8 </td>
      <td> 0.6 </td>
      <td> 0.6 </td>
      <td> 12.4 </td>
      <td> 1.057 </td>
      <td> -0.6 </td>
      <td>  5.2</td>
      <td>  5200</td>
    </tr>
    <tr>
      <th>125</th>
      <td>   Vitali Michele</td>
      <td>      Pasta Reggia Caserta</td>
      <td>     Guardia</td>
      <td> 23</td>
      <td>  ITA</td>
      <td> NaN</td>
      <td> NaN</td>
      <td> NaN</td>
      <td>   NaN</td>
      <td>   NaN</td>
      <td>...</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>   NaN</td>
      <td>    NaN</td>
      <td>   NaN</td>
      <td>  0.0</td>
      <td>     0</td>
    </tr>
    <tr>
      <th>152</th>
      <td>     Spera Andrea</td>
      <td>      Pasta Reggia Caserta</td>
      <td>      Centro</td>
      <td> 18</td>
      <td>  ITA</td>
      <td> NaN</td>
      <td> NaN</td>
      <td> NaN</td>
      <td>   NaN</td>
      <td>   NaN</td>
      <td>...</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>  NaN</td>
      <td>   NaN</td>
      <td>    NaN</td>
      <td>   NaN</td>
      <td>  0.0</td>
      <td>     0</td>
    </tr>
    <tr>
      <th>170</th>
      <td>     Imbrò Matteo</td>
      <td>         Granarolo Bologna</td>
      <td>   Playmaker</td>
      <td> 21</td>
      <td>  ITA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  5.8 </td>
      <td> 15.0 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.2 </td>
      <td> 0.6 </td>
      <td> 1.0 </td>
      <td> 1.4 </td>
      <td>  7.2 </td>
      <td> 1.272 </td>
      <td>  1.8 </td>
      <td>  4.8</td>
      <td>  4800</td>
    </tr>
    <tr>
      <th>191</th>
      <td>       Moss David</td>
      <td> EA7 Emporio Armani Milano</td>
      <td>         Ala</td>
      <td> 31</td>
      <td>  USA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  8.0 </td>
      <td> 26.5 </td>
      <td>...</td>
      <td> 0.3 </td>
      <td> 0.3 </td>
      <td> 0.3 </td>
      <td> 1.0 </td>
      <td> 1.5 </td>
      <td>  7.3 </td>
      <td> 0.917 </td>
      <td>  2.3 </td>
      <td>  9.3</td>
      <td>  9300</td>
    </tr>
    <tr>
      <th>199</th>
      <td>     Gigli Angelo</td>
      <td> EA7 Emporio Armani Milano</td>
      <td>      Centro</td>
      <td> 31</td>
      <td>  RSA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  0.0 </td>
      <td>  6.0 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td>  0.0 </td>
      <td> 0.000 </td>
      <td>  0.0 </td>
      <td> -3.0</td>
      <td>    -3</td>
    </tr>
    <tr>
      <th>200</th>
      <td>   Harper Demonte</td>
      <td>             Enel Brindisi</td>
      <td> Guardia/Ala</td>
      <td> 25</td>
      <td>  USA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  8.4 </td>
      <td> 20.8 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 3.0 </td>
      <td> 0.6 </td>
      <td> 1.2 </td>
      <td>  5.0 </td>
      <td> 0.813 </td>
      <td> -1.2 </td>
      <td>  4.8</td>
      <td>  4800</td>
    </tr>
    <tr>
      <th>216</th>
      <td>  Ruzzier Michele</td>
      <td>       Umana Reyer Venezia</td>
      <td>   Playmaker</td>
      <td> 22</td>
      <td>  ITA</td>
      <td>    </td>
      <td>    </td>
      <td>    </td>
      <td>  3.8 </td>
      <td> 15.2 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.4 </td>
      <td> 0.4 </td>
      <td> 0.2 </td>
      <td> 2.0 </td>
      <td>  1.6 </td>
      <td> 0.710 </td>
      <td>  1.8 </td>
      <td>  5.4</td>
      <td>  5400</td>
    </tr>
  </tbody>
</table>
<p>13 rows × 35 columns</p>
</div>




    # Save my team:
    
    with open("myteam.csv", "w") as f:
        my_team.to_csv(f)


    



    # Round 6


    import pandas as pd
    import numpy as np
    
    !ls
    
    CSV_FILE_NAME = 'profiles_6.csv'
    CSV_FILE_OUT = 'myteam_6.csv'

    1_get_players.py  README.md         myteam_6.csv      players.csv.bak
    1_teambuild.ipynb calendar.csv      [31mnotebook.sh[m[m       profiles.csv.bak
    2_get_profiles.py myteam.csv        players.csv       profiles_6.csv



    df = pd.read_csv(CSV_FILE_NAME, sep=',')
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
    
    # Want to be sure the evaluation is an integer.
    df.Lega = df.Lega.apply(to_int)
    
    def best_by_role(data, role, nret=5):
        """ returns a dataframe filtered by role and 
            sorted by the evaluation assigned.
            
            :param data, dataframe of players.
            :param role, str with the role (eg: player)
            :param nret int, number of player in the output dataframe.
        """
        player = data[data['Role'].isin(role)]
        
        # score must be integer
        return player.sort(['Lega'], ascending=[False])[:nret]


    # compute price
    f = lambda x: x * 1000 if x >0 else 0
    
    df['Price'] = df.Lega.apply(f)
    # filter not used columns:
    
    df_small = df[["Name", "Team", "Role", "Age", "Lega", "Price"]]


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
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>30 </th>
      <td>   Cinciarini Andrea</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td>    Playmaker</td>
      <td> 28</td>
      <td> 20.8</td>
      <td> 20800</td>
    </tr>
    <tr>
      <th>80 </th>
      <td>        Dyson Jerome</td>
      <td> Banco di Sardegna Sassari</td>
      <td> Play/Guardia</td>
      <td> 27</td>
      <td> 19.6</td>
      <td> 19600</td>
    </tr>
    <tr>
      <th>160</th>
      <td>         Vitali Luca</td>
      <td>            Vanoli Cremona</td>
      <td> Play/Guardia</td>
      <td> 28</td>
      <td> 16.0</td>
      <td> 16000</td>
    </tr>
    <tr>
      <th>214</th>
      <td>      Robinson Dawan</td>
      <td>       Openjobmetis Varese</td>
      <td>    Playmaker</td>
      <td> 33</td>
      <td> 15.6</td>
      <td> 15600</td>
    </tr>
    <tr>
      <th>19 </th>
      <td> Johnson-Odom Darius</td>
      <td>   Acqua Vitasnella CantÃ¹</td>
      <td>    Playmaker</td>
      <td> 25</td>
      <td> 14.8</td>
      <td> 14800</td>
    </tr>
  </tbody>
</table>
</div>




    my_team = pd.DataFrame(["Name", "Team", "Role", "Age", "Lega", "Price"])
    
    playmaker = best_by_role(df_small, ['Playmaker', 'Play/Guardia'], 1000)
    ala = best_by_role(df_small, ['Guardia', 'Guardia/Ala', 'Ala/Centro'], 1000)
    centro = best_by_role(df_small, ['Centro', 'Ala/Centro'], 1000)
    
    tot_price = 0
    
    playmaker[playmaker.Price <= 70000/5][:3]




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>82 </th>
      <td>      Hayes Kenny</td>
      <td>       Vanoli Cremona</td>
      <td> Play/Guardia</td>
      <td> 27</td>
      <td> 13.4</td>
      <td> 13400</td>
    </tr>
    <tr>
      <th>29 </th>
      <td> Ferguson Jazzmar</td>
      <td>       Vanoli Cremona</td>
      <td> Play/Guardia</td>
      <td> 27</td>
      <td> 11.8</td>
      <td> 11800</td>
    </tr>
    <tr>
      <th>189</th>
      <td>     Moore Ronald</td>
      <td> Pasta Reggia Caserta</td>
      <td>    Playmaker</td>
      <td> 26</td>
      <td> 10.8</td>
      <td> 10800</td>
    </tr>
  </tbody>
</table>
</div>




    ala[ala.Price <= 70000/5][:5]




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>177</th>
      <td>   Rautins Andy</td>
      <td>       Openjobmetis Varese</td>
      <td> Guardia</td>
      <td> 28</td>
      <td> 13.8</td>
      <td> 13800</td>
    </tr>
    <tr>
      <th>221</th>
      <td>  Taylor Donell</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td> Guardia</td>
      <td> 32</td>
      <td> 13.0</td>
      <td> 13000</td>
    </tr>
    <tr>
      <th>192</th>
      <td>  Turner Elston</td>
      <td>             Enel Brindisi</td>
      <td> Guardia</td>
      <td> 24</td>
      <td> 13.0</td>
      <td> 13000</td>
    </tr>
    <tr>
      <th>33 </th>
      <td> Feldeine James</td>
      <td>   Acqua Vitasnella CantÃ¹</td>
      <td> Guardia</td>
      <td> 26</td>
      <td> 13.0</td>
      <td> 13000</td>
    </tr>
    <tr>
      <th>167</th>
      <td>    Gibson Kyle</td>
      <td>                 Acea Roma</td>
      <td> Guardia</td>
      <td> 27</td>
      <td> 12.8</td>
      <td> 12800</td>
    </tr>
  </tbody>
</table>
</div>




    centro[centro.Price<=70000/5][:5]




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>120</th>
      <td>  Cervi Riccardo</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td>     Centro</td>
      <td> 23</td>
      <td> 12.4</td>
      <td> 12400</td>
    </tr>
    <tr>
      <th>65 </th>
      <td> Ortner Benjamin</td>
      <td>       Umana Reyer Venezia</td>
      <td>     Centro</td>
      <td> 32</td>
      <td> 11.0</td>
      <td> 11000</td>
    </tr>
    <tr>
      <th>45 </th>
      <td> Mazzola Valerio</td>
      <td>         Granarolo Bologna</td>
      <td> Ala/Centro</td>
      <td> 27</td>
      <td> 10.4</td>
      <td> 10400</td>
    </tr>
    <tr>
      <th>44 </th>
      <td>    Ivanov Dejan</td>
      <td>             Enel Brindisi</td>
      <td>     Centro</td>
      <td> 29</td>
      <td> 10.4</td>
      <td> 10400</td>
    </tr>
    <tr>
      <th>108</th>
      <td>      Owens Josh</td>
      <td>   Dolomiti Energia Trento</td>
      <td> Ala/Centro</td>
      <td> 26</td>
      <td> 10.4</td>
      <td> 10400</td>
    </tr>
  </tbody>
</table>
</div>




    playmaker[playmaker.Price <= 20000/5][:5]




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>126</th>
      <td>           Pecile Andrea</td>
      <td>       Upea Capo d'Orlando</td>
      <td> Playmaker</td>
      <td> 35</td>
      <td> 2.6</td>
      <td> 2600</td>
    </tr>
    <tr>
      <th>20 </th>
      <td> Cournooh David Reginald</td>
      <td>             Enel Brindisi</td>
      <td> Playmaker</td>
      <td> 24</td>
      <td> 2.6</td>
      <td> 2600</td>
    </tr>
    <tr>
      <th>92 </th>
      <td>        Mussini Federico</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td> Playmaker</td>
      <td> 18</td>
      <td> 2.5</td>
      <td> 2500</td>
    </tr>
    <tr>
      <th>22 </th>
      <td>         Meacham Trenton</td>
      <td> EA7 Emporio Armani Milano</td>
      <td> Playmaker</td>
      <td> 29</td>
      <td> 2.4</td>
      <td> 2400</td>
    </tr>
    <tr>
      <th>124</th>
      <td>       Tommasini Claudio</td>
      <td>      Pasta Reggia Caserta</td>
      <td> Playmaker</td>
      <td> 23</td>
      <td> 2.0</td>
      <td> 2000</td>
    </tr>
  </tbody>
</table>
</div>




    ala[ala.Price <=  20000/5][:5]




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>93 </th>
      <td>    Mordente Marco</td>
      <td> Pasta Reggia Caserta</td>
      <td>     Guardia</td>
      <td> 36</td>
      <td> 4.0</td>
      <td> 4000</td>
    </tr>
    <tr>
      <th>128</th>
      <td> De Gennaro Matteo</td>
      <td>        Enel Brindisi</td>
      <td>     Guardia</td>
      <td> 18</td>
      <td> 3.0</td>
      <td> 3000</td>
    </tr>
    <tr>
      <th>180</th>
      <td>  Michelori Andrea</td>
      <td> Pasta Reggia Caserta</td>
      <td>  Ala/Centro</td>
      <td> 37</td>
      <td> 2.6</td>
      <td> 2600</td>
    </tr>
    <tr>
      <th>164</th>
      <td>   Raspino Tommaso</td>
      <td> Consultinvest Pesaro</td>
      <td> Guardia/Ala</td>
      <td> 25</td>
      <td> 2.0</td>
      <td> 2000</td>
    </tr>
    <tr>
      <th>105</th>
      <td>      Gaines Frank</td>
      <td> Pasta Reggia Caserta</td>
      <td>     Guardia</td>
      <td> 24</td>
      <td> 1.8</td>
      <td> 1800</td>
    </tr>
  </tbody>
</table>
</div>




    centro[centro.Price<=20000/5][:5]




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>156</th>
      <td>    Cuccarolo Gino</td>
      <td>    Granarolo Bologna</td>
      <td>     Centro</td>
      <td> 27</td>
      <td> 3.0</td>
      <td> 3000</td>
    </tr>
    <tr>
      <th>180</th>
      <td>  Michelori Andrea</td>
      <td> Pasta Reggia Caserta</td>
      <td> Ala/Centro</td>
      <td> 37</td>
      <td> 2.6</td>
      <td> 2600</td>
    </tr>
    <tr>
      <th>17 </th>
      <td>       Cusin Marco</td>
      <td>       Vanoli Cremona</td>
      <td>     Centro</td>
      <td> 30</td>
      <td> 2.5</td>
      <td> 2500</td>
    </tr>
    <tr>
      <th>85 </th>
      <td>   Lechthaler Luca</td>
      <td>     Sidigas Avellino</td>
      <td>     Centro</td>
      <td> 29</td>
      <td> 1.6</td>
      <td> 1600</td>
    </tr>
    <tr>
      <th>61 </th>
      <td> Cattapan Riccardo</td>
      <td>    Granarolo Bologna</td>
      <td>     Centro</td>
      <td> 17</td>
      <td> 0.0</td>
      <td>    0</td>
    </tr>
  </tbody>
</table>
</div>




    playmaker[playmaker.Price <= 10000/3][:5]




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>126</th>
      <td>           Pecile Andrea</td>
      <td>       Upea Capo d'Orlando</td>
      <td> Playmaker</td>
      <td> 35</td>
      <td> 2.6</td>
      <td> 2600</td>
    </tr>
    <tr>
      <th>20 </th>
      <td> Cournooh David Reginald</td>
      <td>             Enel Brindisi</td>
      <td> Playmaker</td>
      <td> 24</td>
      <td> 2.6</td>
      <td> 2600</td>
    </tr>
    <tr>
      <th>92 </th>
      <td>        Mussini Federico</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td> Playmaker</td>
      <td> 18</td>
      <td> 2.5</td>
      <td> 2500</td>
    </tr>
    <tr>
      <th>22 </th>
      <td>         Meacham Trenton</td>
      <td> EA7 Emporio Armani Milano</td>
      <td> Playmaker</td>
      <td> 29</td>
      <td> 2.4</td>
      <td> 2400</td>
    </tr>
    <tr>
      <th>124</th>
      <td>       Tommasini Claudio</td>
      <td>      Pasta Reggia Caserta</td>
      <td> Playmaker</td>
      <td> 23</td>
      <td> 2.0</td>
      <td> 2000</td>
    </tr>
  </tbody>
</table>
</div>




    ala[ala.Price<=10000/3][:5]




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>128</th>
      <td> De Gennaro Matteo</td>
      <td>        Enel Brindisi</td>
      <td>     Guardia</td>
      <td> 18</td>
      <td> 3.0</td>
      <td> 3000</td>
    </tr>
    <tr>
      <th>180</th>
      <td>  Michelori Andrea</td>
      <td> Pasta Reggia Caserta</td>
      <td>  Ala/Centro</td>
      <td> 37</td>
      <td> 2.6</td>
      <td> 2600</td>
    </tr>
    <tr>
      <th>164</th>
      <td>   Raspino Tommaso</td>
      <td> Consultinvest Pesaro</td>
      <td> Guardia/Ala</td>
      <td> 25</td>
      <td> 2.0</td>
      <td> 2000</td>
    </tr>
    <tr>
      <th>105</th>
      <td>      Gaines Frank</td>
      <td> Pasta Reggia Caserta</td>
      <td>     Guardia</td>
      <td> 24</td>
      <td> 1.8</td>
      <td> 1800</td>
    </tr>
    <tr>
      <th>201</th>
      <td>    Sandri Daniele</td>
      <td>            Acea Roma</td>
      <td>     Guardia</td>
      <td> 24</td>
      <td> 1.4</td>
      <td> 1400</td>
    </tr>
  </tbody>
</table>
</div>




    centro[centro.Price<=10000/3][:5]




<div style="max-height:1000px;max-width:1500px;overflow:auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Team</th>
      <th>Role</th>
      <th>Age</th>
      <th>Lega</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>156</th>
      <td>    Cuccarolo Gino</td>
      <td>    Granarolo Bologna</td>
      <td>     Centro</td>
      <td> 27</td>
      <td> 3.0</td>
      <td> 3000</td>
    </tr>
    <tr>
      <th>180</th>
      <td>  Michelori Andrea</td>
      <td> Pasta Reggia Caserta</td>
      <td> Ala/Centro</td>
      <td> 37</td>
      <td> 2.6</td>
      <td> 2600</td>
    </tr>
    <tr>
      <th>17 </th>
      <td>       Cusin Marco</td>
      <td>       Vanoli Cremona</td>
      <td>     Centro</td>
      <td> 30</td>
      <td> 2.5</td>
      <td> 2500</td>
    </tr>
    <tr>
      <th>85 </th>
      <td>   Lechthaler Luca</td>
      <td>     Sidigas Avellino</td>
      <td>     Centro</td>
      <td> 29</td>
      <td> 1.6</td>
      <td> 1600</td>
    </tr>
    <tr>
      <th>61 </th>
      <td> Cattapan Riccardo</td>
      <td>    Granarolo Bologna</td>
      <td>     Centro</td>
      <td> 17</td>
      <td> 0.0</td>
      <td>    0</td>
    </tr>
  </tbody>
</table>
</div>




    # My Team
    
    my_team = df[df.Name.isin (
    ['Johnson-Odom Darius',
     'Kaukenas Rimantas',
     'Rautins Andy',
     'Hunt Dario',
     'Cervi Riccardo',
     'Pecile Andrea',
     'Mordente Marco',
     'De Gennaro Matteo',
     'Cuccarolo Gino',
     'Michelori Andrea',
     'D\'Ercole Lorenzo',
     'Okoye Stanley',
     'Cusin Marco'
    ])]
    
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
      <th>17 </th>
      <td>         Cusin Marco</td>
      <td>            Vanoli Cremona</td>
      <td>       Centro</td>
      <td> 30</td>
      <td>  ITA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td>  1.0 </td>
      <td>  5.5 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.5 </td>
      <td>  2.5</td>
      <td> 1.000 </td>
      <td>  0.5 </td>
      <td> -2.5 </td>
      <td>  2500</td>
    </tr>
    <tr>
      <th>19 </th>
      <td> Johnson-Odom Darius</td>
      <td>   Acqua Vitasnella CantÃ¹</td>
      <td>    Playmaker</td>
      <td> 25</td>
      <td>  USA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td> 16.8 </td>
      <td> 32.2 </td>
      <td>...</td>
      <td> 0.2 </td>
      <td> 0.8 </td>
      <td> 4.4 </td>
      <td> 1.2 </td>
      <td> 5.0 </td>
      <td> 14.8</td>
      <td> 0.820 </td>
      <td>  1.8 </td>
      <td>  2.8 </td>
      <td> 14800</td>
    </tr>
    <tr>
      <th>93 </th>
      <td>      Mordente Marco</td>
      <td>      Pasta Reggia Caserta</td>
      <td>      Guardia</td>
      <td> 36</td>
      <td>  ITA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td>  3.8 </td>
      <td> 24.2 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.2 </td>
      <td> 1.4 </td>
      <td> 0.6 </td>
      <td> 1.4 </td>
      <td>  4.0</td>
      <td> 0.727 </td>
      <td>  0.6 </td>
      <td> -3.0 </td>
      <td>  4000</td>
    </tr>
    <tr>
      <th>99 </th>
      <td>    D'Ercole Lorenzo</td>
      <td>                 Acea Roma</td>
      <td> Play/Guardia</td>
      <td> 27</td>
      <td>     </td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td>  1.8 </td>
      <td> 17.6 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.4 </td>
      <td> 1.0 </td>
      <td> 0.4 </td>
      <td>  1.0</td>
      <td> 0.539 </td>
      <td>  1.0 </td>
      <td> -7.0 </td>
      <td>  1000</td>
    </tr>
    <tr>
      <th>115</th>
      <td>   Kaukenas Rimantas</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td>      Guardia</td>
      <td> 38</td>
      <td>  LIT</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td> 16.0 </td>
      <td> 30.6 </td>
      <td>...</td>
      <td> 0.2 </td>
      <td> 0.0 </td>
      <td> 3.0 </td>
      <td> 1.2 </td>
      <td> 2.6 </td>
      <td> 14.6</td>
      <td> 1.180 </td>
      <td>  0.8 </td>
      <td>  4.2 </td>
      <td> 14600</td>
    </tr>
    <tr>
      <th>120</th>
      <td>      Cervi Riccardo</td>
      <td> Grissin Bon Reggio Emilia</td>
      <td>       Centro</td>
      <td> 23</td>
      <td>  ITA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td>  9.2 </td>
      <td> 26.6 </td>
      <td>...</td>
      <td> 1.8 </td>
      <td> 0.4 </td>
      <td> 1.8 </td>
      <td> 0.6 </td>
      <td> 0.6 </td>
      <td> 12.4</td>
      <td> 1.057 </td>
      <td> -0.6 </td>
      <td>  5.2 </td>
      <td> 12400</td>
    </tr>
    <tr>
      <th>121</th>
      <td>          Hunt Dario</td>
      <td>       Upea Capo d'Orlando</td>
      <td>       Centro</td>
      <td> 25</td>
      <td>  USA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td> 12.0 </td>
      <td> 25.2 </td>
      <td>...</td>
      <td> 0.8 </td>
      <td> 0.6 </td>
      <td> 2.6 </td>
      <td> 0.4 </td>
      <td> 1.2 </td>
      <td> 14.4</td>
      <td> 0.940 </td>
      <td> -1.0 </td>
      <td> -2.8 </td>
      <td> 14400</td>
    </tr>
    <tr>
      <th>126</th>
      <td>       Pecile Andrea</td>
      <td>       Upea Capo d'Orlando</td>
      <td>    Playmaker</td>
      <td> 35</td>
      <td>  ITA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td>  2.6 </td>
      <td> 16.6 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.4 </td>
      <td> 1.0 </td>
      <td> 0.2 </td>
      <td> 1.0 </td>
      <td>  2.6</td>
      <td> 0.341 </td>
      <td>  0.2 </td>
      <td> -2.2 </td>
      <td>  2600</td>
    </tr>
    <tr>
      <th>128</th>
      <td>   De Gennaro Matteo</td>
      <td>             Enel Brindisi</td>
      <td>      Guardia</td>
      <td> 18</td>
      <td>  ITA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td>  3.0 </td>
      <td>  2.0 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td>  3.0</td>
      <td> 3.000 </td>
      <td>  0.0 </td>
      <td>  4.0 </td>
      <td>  3000</td>
    </tr>
    <tr>
      <th>156</th>
      <td>      Cuccarolo Gino</td>
      <td>         Granarolo Bologna</td>
      <td>       Centro</td>
      <td> 27</td>
      <td>  ITA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td>  2.4 </td>
      <td>  7.2 </td>
      <td>...</td>
      <td> 0.4 </td>
      <td> 0.0 </td>
      <td> 1.2 </td>
      <td> 0.0 </td>
      <td> 0.2 </td>
      <td>  3.0</td>
      <td> 0.603 </td>
      <td> -1.0 </td>
      <td> -2.2 </td>
      <td>  3000</td>
    </tr>
    <tr>
      <th>177</th>
      <td>        Rautins Andy</td>
      <td>       Openjobmetis Varese</td>
      <td>      Guardia</td>
      <td> 28</td>
      <td>  USA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td> 15.8 </td>
      <td> 32.4 </td>
      <td>...</td>
      <td> 0.0 </td>
      <td> 0.0 </td>
      <td> 1.4 </td>
      <td> 1.2 </td>
      <td> 1.2 </td>
      <td> 13.8</td>
      <td> 1.138 </td>
      <td>  1.0 </td>
      <td>  1.4 </td>
      <td> 13800</td>
    </tr>
    <tr>
      <th>178</th>
      <td>       Okoye Stanley</td>
      <td>       Openjobmetis Varese</td>
      <td>          Ala</td>
      <td> 24</td>
      <td>  USA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td>  6.5 </td>
      <td> 18.8 </td>
      <td>...</td>
      <td> 0.3 </td>
      <td> 0.5 </td>
      <td> 1.3 </td>
      <td> 0.0 </td>
      <td> 0.8 </td>
      <td>  8.0</td>
      <td> 1.013 </td>
      <td> -0.5 </td>
      <td>  3.0 </td>
      <td>  8000</td>
    </tr>
    <tr>
      <th>180</th>
      <td>    Michelori Andrea</td>
      <td>      Pasta Reggia Caserta</td>
      <td>   Ala/Centro</td>
      <td> 37</td>
      <td>  ITA</td>
      <td>  </td>
      <td>  </td>
      <td>  </td>
      <td>  4.0 </td>
      <td> 15.8 </td>
      <td>...</td>
      <td> 0.4 </td>
      <td> 0.6 </td>
      <td> 1.2 </td>
      <td> 1.0 </td>
      <td> 0.4 </td>
      <td>  2.6</td>
      <td> 0.630 </td>
      <td>  0.2 </td>
      <td>  1.4 </td>
      <td>  2600</td>
    </tr>
  </tbody>
</table>
<p>13 rows × 35 columns</p>
</div>




    ## Team value 


    sum(my_team.Price)




    96700.0




    # Save my team:
    
    with open(CSV_FILE_OUT, "w") as f:
        my_team.to_csv(f)


    


    


    

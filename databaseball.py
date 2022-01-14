from turtle import color
from h2o_wave import main, app, Q, ui, data
import pandas as pd

players = [["Ted Williams", "tedWil"], ["Mike Trout", 'trout'], ['Jackie Robinson', 'robinson'], ['Albert Pujols', 'pujols'], ['Babe Ruth', 'ruth'], ['Hank Aaron', 'aaron'], ['Larry Walker', 'walker'], ['Tip O\'Neill', 'oneill']]
    
stategories = ['Year', 'Age', 'Games', 'PA', 'AB', 'H', 'BA', 'HR', 'RBI', 'OBP', 'SLG', 'OPS', 'OPS_Plus']
stategories_proper_text = dict(zip(stategories, 
                                    [stat if stat != 'OPS_Plus' else 'OPS+' for stat in stategories]))




player_sheets = {}
qq_sheets = {}

def load_data(file):
    data = pd.read_csv(f'player_data/{file}.csv', na_filter=False)
    return data

def QQ_metric(ops_plus, pa):
    return round( ops_plus*(-2**(-(pa/112))+1)**6 )

for player in players:
    loaded_data = load_data(player[1])
    loaded_data = loaded_data.rename(columns={"G": "Games"})
    player_sheets.setdefault(player[0], loaded_data.loc[:len(loaded_data), stategories])

    qq_data = {
        "Year": player_sheets[player[0]]["Year"],
        "Age": player_sheets[player[0]]["Age"],
        "QQ Metric": [QQ_metric(a,b) for a,b in zip(player_sheets[player[0]]['OPS_Plus'], 
                                                    player_sheets[player[0]]['PA'])],
        "PA": player_sheets[player[0]]["PA"],
        "OPS+": player_sheets[player[0]]["OPS_Plus"],
        
    }
    qq_sheets.setdefault(player[0], pd.DataFrame(qq_data))




@app('/databaseball')
async def serve(q:Q):
    if not q.client.initialized:
        initialize_ui(q)
        q.client.stat_category = 'HR'
        q.client.time = 'Age'
        q.client.player = 'Ted Williams'
        q.client.df = player_sheets[q.client.player]
        q.client.df_qq = qq_sheets[q.client.player]
        graph_view(q, q.client.df)
        qq_table(q, q.client.df_qq)
    
    if q.args.player_dropdown == q.client.player:
        q.args.player_dropdown = None

    if q.args.graph:
        graph_view(q, q.client.df)   
    elif q.args.table:
        table_view(q, q.client.df)    
    elif q.args.player_dropdown:
        q.client.player = q.args.player_dropdown
        q.client.df = player_sheets[q.client.player]
        q.client.df_qq = qq_sheets[q.client.player]
        updateTabs(q)
        graph_view(q, q.client.df)  
        qq_table(q, q.client.df_qq)
    elif q.args.stat_category or q.args.time:
        q.client.stat_category = q.args.stat_category
        q.client.time = q.args.time
        graph_view(q, q.client.df)
    
    q.args.player_dropdown = None 
    await q.page.save()
        
def updateTabs(q):
    q.page['tabs'] = ui.tab_card(
    box = 'tabs',
    items=[
        ui.tab(name="graph", label="Graph View"),
        ui.tab(name="table", label="Table View")
    ]
    )

def initialize_ui(q):
    q.page['meta'] = ui.meta_card(
        box="",
        layouts=[
            ui.layout(
                breakpoint="xs",
                zones=[
                    ui.zone('entirePage',  direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('universal', direction=ui.ZoneDirection.COLUMN, size="45%", zones=[
                            ui.zone('header',size="10%"),
                            ui.zone('players'),
                            ui.zone('qq_header', size = '10%'),
                            ui.zone('qq_data')
                        ]),

                        ui.zone('stats', size="70%", zones=[
                            ui.zone('tabs'),
                            ui.zone('data')

                        ]),
                        
                        ]),
                    ui.zone('footer'),
                ]
            )
        ]
    )

    q.page['title'] = ui.header_card(
        box='header',
        title='Database-ball',
        subtitle="The data behind legendary baseball careers",
        icon='Baseball',
        icon_color='$white',
    )
    
    q.page['qq_title'] = ui.form_card(
        box='qq_header', 
        items=[
            ui.text_xl('Quality/Quantity (QQ Metric) performance timeline',
            ),
        ]
    )
    updateTabs(q)


    q.client.initialized = True
    


def qq_table(q, df_qq):
    # print("creating qq_table")
    q.page['players'] = ui.form_card(
        box="players",
        items=[
            ui.dropdown(
                name='player_dropdown',
                label='Select Player',               
                choices=[
                    ui.choice(name=player[0], label=player[0]) for player in players
                ],
                trigger=True,
                value=q.client.player,
            )
        ]
    )

    q.page["qq_table"] = ui.form_card(
        box='qq_data', 
        items=[
            ui.table(
                name='qq table',
                columns=[ui.table_column(name=col, label=col) for col in df_qq.columns],
                rows=[ui.table_row(
                    name=str(i),
                    cells=[str(df_qq[col].values[i]) for col in df_qq.columns]
                )
                for i in range(len(df_qq))],
                downloadable = True,
            )
    ])


def table_view(q, df):
    del q.page["graph_view"], q.page["statsDropdown"]
    q.page['table_view'] = ui.form_card(
        box='data', 
        items=[
            ui.table(
                name='table example',
                columns=[ui.table_column(name=col, label=col) for col in stategories_proper_text.values()],
                rows=[ui.table_row(
                    name=str(i),
                    cells=[str(df[col].values[i]) for col in df.columns]
                )
                for i in range(len(df))],
                downloadable = True,
                # height='1000px'
            )
    ])


def graph_view(q, df):
    del q.page["table_view"]

    q.page['statsDropdown'] = ui.form_card(
        box="data",
        items=[
            ui.inline(items=[
                ui.dropdown(
                    name='stat_category',
                    label='y-axis (Stat Category)',                   
                    choices=[
                        ui.choice(name=col, label=stategories_proper_text[col]) for col in df.columns.values[2:]
                    ],
                    width='300px',
                    trigger=True,
                    value=q.client.stat_category,
                ),

                ui.dropdown(
                    name='time',
                    label='x-axis (Time)',                   
                    choices=[
                        ui.choice(name=col, label=col) for col in ['Year','Age']
                    ],
                    trigger=True,
                    value=q.client.time,
                )
            ])
        ]
    )

    q.page['graph_view']= ui.plot_card(
        box = 'data',
        title=f'{q.client.player}\'s {stategories_proper_text[q.client.stat_category]}',
        data=data(fields=df.columns.tolist(),rows = df.values.tolist()[:-2]),
        plot = ui.plot(marks=[ui.mark(
            type='interval',
            x=f'={q.client.time}',
            y=f'={q.client.stat_category}',
            x_title=q.client.time,
            y_title=stategories_proper_text[q.client.stat_category]
        ),
        ])
    )

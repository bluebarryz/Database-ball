from h2o_wave import main, app, Q, ui, data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    data = pd.read_csv('player_data/tedWil.csv',na_filter=False)
    return data

df = load_data()

@app('/databaseball')
async def serve(q:Q):

    if not q.client.initialized:
        initialize_ui(q)
        graph_view(q)
    if q.args.graph:
        graph_view(q)
    elif q.args.table:
        table_view(q)
    elif q.args.stat_category or q.args.time:
        q.client.stat_category = q.args.stat_category
        q.client.time = q.args.time
        graph_view(q)

    await q.page.save()
        


def initialize_ui(q):
    q.page['meta'] = ui.meta_card(
        box="",
        layouts=[
            ui.layout(
                breakpoint="xs",
                zones=[
                    ui.zone('entirePage',  direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('universal', direction=ui.ZoneDirection.COLUMN, size="25%", zones=[
                            ui.zone('header'),
                            ui.zone('links'),
                        ]),

                        # ui.zone('stats', size="70%"),

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

    q.page['links'] = ui.form_card(
        box='links',
        items=[
            ui.link(label='Ted Williams', path='/ted_williams'),
            ui.link(label='Mike Trout', path='/mike_trout'),
            ui.link(label='Internal link, new tab', path='/starred', target='_blank'),  # same as target=''
            ui.link(label='Internal link, disabled', path='/starred', disabled=True),
            ui.link(label='External link', path='https://h2o.ai'),
            ui.link(label='External link, new tab', path='https://h2o.ai', target=''),
            ui.link(label='External link, new tab', path='https://h2o.ai', target='_blank'),  # same as target=''
            ui.link(label='External link, disabled', path='https://h2o.ai', disabled=True),
            ui.link(label='Download link', path='https://file-examples-com.github.io/uploads/2017/02/file-sample_100kB.doc', download=True),
        ]
    )

    q.page['tabs'] = ui.tab_card(
        box = 'tabs',
        items=[
            ui.tab(name="graph", label="Graph View"),
            ui.tab(name="table", label="Table View")
        ]
    )
    q.client.initialized = True
    q.client.stat_category = 'HR'
    q.client.time = 'Age'


def table_view(q):
    del q.page["graph_view"], q.page["statsDropdown"]

    q.page['table_view'] = ui.form_card(
        box='data', 
        items=[
            ui.table(
                name='table example',
                columns=[ui.table_column(name=col, label=col) for col in df.columns.values],
                rows=[ui.table_row(
                    name=str(i),
                    cells=[str(df[col].values[i]) for col in df.columns.values]
                )
                for i in range(len(df))],
                downloadable = True
                # height='1000px'
            )
    ])


df_bar = df.loc[:18, ['Year', 'BA', 'HR', 'RBI', 'OBP', 'SLG', 'OPS', 'OPS_Plus', 'Age']]


def graph_view(q):
    del q.page["table_view"]

    q.page['statsDropdown'] = ui.form_card(
        box="data",
        items=[
            ui.inline(items=[
                ui.dropdown(
                    name='stat_category',
                    label='y-axis (Stat Category)',
                    value=q.client.stat_category,
                    choices=[
                        ui.choice(name=col, label=col) for col in df_bar.columns.values[1:]
                    ],
                    width='300px',
                    trigger=True
                ),

                ui.dropdown(
                    name='time',
                    label='x-axis (Time)',
                    value=q.client.time,
                    choices=[
                        ui.choice(name=col, label=col) for col in ['Year','Age']
                    ],
                    trigger=True
                )
            ])
        ]
    )
    print(q.client.time,q.client.stat_category)
    q.page['graph_view']= ui.plot_card(
        box = 'data',
        title=f'Player\'s {q.client.stat_category}',
        data=data(fields=df_bar.columns.tolist(),rows = df_bar.values.tolist()),
        plot = ui.plot(marks=[ui.mark(
            type='interval',
            x=f'={q.client.time}',
            y=f'={q.client.stat_category}',
            x_title=q.client.time,
            y_title=q.client.stat_category
        ),
        ])
    )



                
        





#from matplotlib.figure import Figure
import plotly.express as px
import plotly.graph_objects as go

from collections import OrderedDict
import numpy as np

def make_figure(df,pa):
    """Generates figure.

    Args:
        df (pandas.core.frame.DataFrame): Pandas DataFrame containing the input data.
        pa (dict): A dictionary of the style { "argument":"value"} as outputted by `figure_defaults`.

    Returns:
        A Plotly figure
        
    """

    pa_={}
    for n in ["fig_width","fig_height"]:
        if pa[n] == "":
            pa_[n]=None
        else:
            pa_[n]=float(pa[n])

    tmp=df.copy()
    tmp=tmp[pa["vals"]]

    fig = go.Figure( )
    fig.update_layout( width=pa_["fig_width"], height=pa_["fig_height"] ) #  autosize=False,

    # MAIN FIGURE
    # PLOT ONE HISTOGRAM PER COLUMN SELECTED BY USER
    pab={}
    for arg in ["show_legend","upper_axis","lower_axis","left_axis","right_axis","errorbar","errorbar_symmetric","tick_left_axis","tick_lower_axis","tick_upper_axis","tick_right_axis"]:
        if pa[arg] in ["off",".off"]:
            pab[arg]=False
        else:
            pab[arg]=True

    for h in pa["groups_settings"].values():
        hoverinfo=h["hoverinfo"]
        hover_align=h["hover_align"]
        hover_fontsize=int(h["hover_fontsize"])
        histfunc=h["histfunc"]
        cumulative_direction=h["cumulative_direction"]

        if h["label"]!="":
            name=h["label"]
        else:
            name=""
        
        if h["text"]!="":
            text=h["text"]
        else:
            text=""

        if h["color_rgb"] == "":
            if h["color_value"]=="None":
                marker_color=None
            else:
                marker_color = h["color_value"]
        else:
            marker_color = GET_COLOR( h["color_rgb"] )
                
        if h["line_rgb"] == "":
            if h["line_color"]=="None":
                line_color=None
            else:
                line_color = h["line_color"]
        else:
            line_color = GET_COLOR( h["line_rgb"] )
        
        if h["hover_bgcolor"]=="None":
            hover_bgcolor=None
        else:
            hover_bgcolor = h["hover_bgcolor"]
        
        if h["hover_bordercolor"]=="None":
            hover_bordercolor=None
        else:
            hover_bordercolor = h["hover_bordercolor"]
        
        if h["hover_fontfamily"] == "Default":
            hover_fontfamily= None
        else:
            hover_fontfamily=h["hover_fontfamily"]
        
        if h["hover_fontcolor"]=="None":
            hover_fontcolor=None
        else:
            hover_fontcolor = h["hover_fontcolor"]

        if h["histnorm"] == "None":
            histnorm = ""
        else:
            histnorm = h["histnorm"]
            
        if h["opacity"]!=pa["opacity"]:
            opacity=float(h["opacity"])
        else:
            opacity=float(pa["opacity"])
        
        if h["linewidth"]!=pa["linewidth"]:
            linewidth=float(h["linewidth"])
        else:
            linewidth=float(pa["linewidth"])
        
        if h["density"]=="on":
            pa_["density"]=True
        else:
            pa_["density"]=False

        if h["cumulative"]=="on":
            cumulative_enabled=True
        else:
            cumulative_enabled=False
    
        if h["bins_number"]=="":
            bins_number=None
        else:
            bins_number=int(h["bins_number"])

            
        
        marker=dict(color=marker_color,line=dict(width=linewidth,color=line_color))
        cumulative=dict(enabled=cumulative_enabled,direction=cumulative_direction)

        hoverlabel=dict(bgcolor=hover_bgcolor,bordercolor=hover_bordercolor,align=hover_align,\
            font=dict(family=hover_fontfamily,size=hover_fontsize,color=hover_fontcolor))
        
        if pab["errorbar"]==True:
                errorbar=True
                errorbar_value=float(pa["errorbar_value"])
                errorbar_type=pa["errorbar_type"]
                errorbar_symmetric=pab["errorbar_symmetric"]
                errorbar_thickness=float(pa["errorbar_thickness"])
                errorbar_width=float(pa["errorbar_width"])
                if pa["errorbar_color"]=="None":
                    errorbar_color=None
                else:
                    errorbar_color = pa["errorbar_color"]

        if h["orientation_value"]=="vertical":

            if pab["errorbar"]==True:
                error_y=dict(visible=errorbar,value=errorbar_value,type=errorbar_type,symmetric=errorbar_symmetric,color=errorbar_color,\
                    thickness=errorbar_thickness,width=errorbar_width)
            else:
                error_y=dict(visible=False)
                
            trace=fig.add_trace(go.Histogram(x=tmp[h["name"]],text=text,hoverinfo=hoverinfo,histfunc=histfunc,cumulative=cumulative,\
            opacity=opacity,nbinsx=bins_number,name=name,marker=marker,error_y=error_y,hoverlabel=hoverlabel))


        elif h["orientation_value"]=="horizontal":

            if pab["errorbar"]==True:
                error_x=dict(visible=errorbar,value=errorbar_value,type=errorbar_type,symmetric=errorbar_symmetric,color=errorbar_color,\
                    thickness=errorbar_thickness,width=errorbar_width)
            else:
                error_x=dict(visible=False)
            
            fig.add_trace(go.Histogram(y=tmp[h["name"]],text=text,hoverinfo=hoverinfo,histfunc=histfunc,cumulative=cumulative,\
            opacity=opacity,nbinsy=bins_number,name=name,marker=marker,error_x=error_x,hoverlabel=hoverlabel))



    #UPDATE LAYOUT OF HISTOGRAMS
    #Update title
    if pa["title_fontfamily"]=="Default":
        title_fontfamily=None
    else:
        title_fontfamily=pa["title_fontfamily"]

    if pa["title_fontcolor"]=="None":
        title_fontcolor=None
    else:
        title_fontcolor=pa["title_fontcolor"]

    title_fontsize=int(pa["title_fontsize"])
    xref=pa["xref"]
    yref=pa["yref"]

    title_xanchor=pa["title_xanchor"]
    title_yanchor=pa["title_yanchor"]
    x=float(pa["x"])
    y=float(pa["y"])
        
    title=dict(text=pa["title"],font=dict(family=title_fontfamily,size=title_fontsize,color=title_fontcolor),\
        xref=xref,yref=yref,x=x,y=y,xanchor=title_xanchor,yanchor=title_yanchor)

    fig.update_layout(title=title)

    fig.update_layout(barmode=pa["barmode"])

    if pa["log_scale"]==True and pa["orientation"]=="vertical":
        fig.update_yaxes(type="log")
    elif pa["log_scale"]==True and pa["orientation"]=="horizontal":
        fig.update_xaxes(type="log")

    #Update axes
    if pa["axis_line_color"]=="None":
        linecolor=None
    else:
        linecolor=pa["axis_line_color"]
    fig.update_xaxes(zeroline=False, showline=pab["lower_axis"], linewidth=float(pa["axis_line_width"]), linecolor=linecolor)
    fig.update_yaxes(zeroline=False, showline=pab["left_axis"], linewidth=float(pa["axis_line_width"]), linecolor=linecolor)

    #Update ticks
    if pa["ticks_color"]=="None":
        tickcolor=None
    else:
        tickcolor=pa["ticks_color"]
    if pab["tick_lower_axis"]==False and pab["tick_right_axis"]==False and pab["tick_left_axis"]==False and pab["tick_upper_axis"]==False:
        pa["ticks_direction_value"]=""
        ticks=""
    else:
        ticks=pa["ticks_direction_value"]
    fig.update_xaxes(ticks=ticks, tickwidth=float(pa["ticks_line_width"]), tickcolor=tickcolor, ticklen=float(pa["ticks_length"]))
    fig.update_yaxes(ticks=ticks, tickwidth=float(pa["ticks_line_width"]), tickcolor=tickcolor, ticklen=float(pa["ticks_length"]))

    #Update mirror property of axis based on ticks and axis selected by user
    #Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. 
    # If "True", the axis lines are mirrored. If "ticks", the axis lines and ticks are mirrored. If "False", mirroring is disable. 
    # If "all", axis lines are mirrored on all shared-axes subplots. If "allticks", axis lines and ticks are mirrored on all shared-axes subplots.
    if pab["upper_axis"]==True and pab["tick_upper_axis"]==True:
        fig.update_xaxes(mirror="ticks")
    elif pab["upper_axis"]==True and pab["tick_upper_axis"]==False:
        fig.update_xaxes(mirror=True)
    else:
        fig.update_xaxes(mirror=False)
    
    
    if pab["right_axis"]==True and pab["tick_right_axis"]==True:
        fig.update_yaxes(mirror="ticks")
    elif pab["right_axis"]==True and pab["tick_right_axis"]==False:
        fig.update_yaxes(mirror=True)
    else:
        fig.update_xaxes(mirror=False)

    if (pa["x_lower_limit"]!="") and (pa["x_upper_limit"]!="") :
        xmin=float(pa["x_lower_limit"])
        xmax=float(pa["x_upper_limit"])
        fig.update_xaxes(range=[xmin, xmax])

    if (pa["y_lower_limit"]!="") and (pa["y_upper_limit"]!="") :
        ymin=float(pa["y_lower_limit"])
        ymax=float(pa["y_upper_limit"])
        fig.update_yaxes(range=[ymin, ymax])

    if pa["maxxticks"]!="":
        fig.update_yaxes(nticks=int(pa["maxxticks"]))

    if pa["maxyticks"]!="":
        fig.update_yaxes(nticks=int(pa["maxyticks"]))

    #Update spikes
    if pa["spikes_color"]=="None":
        spikecolor=None
    else:
        spikecolor=pa["spikes_color"]

    spikethickness=float(pa["spikes_thickness"])
    spikedash=pa["spikes_dash"]
    spikemode=pa["spikes_mode"]
    
    if pa["spikes_value"]=="both":
        fig.update_xaxes(showspikes=True,spikecolor=spikecolor,spikethickness=spikethickness,spikedash=spikedash,spikemode=spikemode)
        fig.update_yaxes(showspikes=True,spikecolor=spikecolor,spikethickness=spikethickness,spikedash=spikedash,spikemode=spikemode)
   
    elif pa["spikes_value"]=="x":
        fig.update_xaxes(showspikes=True,spikecolor=spikecolor,spikethickness=spikethickness,spikedash=spikedash,spikemode=spikemode)   
    
    elif pa["spikes_value"]=="y":
        fig.update_yaxes(showspikes=True,spikecolor=spikecolor,spikethickness=spikethickness,spikedash=spikedash,spikemode=spikemode)   

    elif pa["spikes_value"]=="None":
        fig.update_xaxes(showspikes=None)
        fig.update_yaxes(showspikes=None)


    #UPDATE X AXIS AND Y AXIS LAYOUT
    xlabel=pa["xlabel"]
    ylabel=pa["ylabel"]
    xlabel_fontsize=int(pa["label_fontsize"])
    ylabel_fontsize=int(pa["label_fontsize"])

    if pa["label_fontfamily"]=="Default":
        xlabel_fontfamily=None
    else:
        xlabel_fontfamily=pa["label_fontfamily"]

    if pa["label_fontfamily"]=="Default":
        ylabel_fontfamily=None
    else:
        ylabel_fontfamily=pa["label_fontfamily"]

    if pa["label_fontcolor"]=="None":
        xlabel_fontcolor=None
    else:
        xlabel_fontcolor = pa["label_fontcolor"]

    if pa["label_fontcolor"]=="None":
        ylabel_fontcolor=None
    else:
        ylabel_fontcolor = pa["label_fontcolor"]

    if pa["paper_bgcolor"]=="None":
        paper_bgcolor=None
    else:
        paper_bgcolor=pa["paper_bgcolor"]
    if pa["plot_bgcolor"]=="None":
        plot_bgcolor=None
    else:
        plot_bgcolor=pa["plot_bgcolor"]    
    
    xaxis=dict(visible=True, title=dict(text=xlabel,font=dict(family=xlabel_fontfamily,size=xlabel_fontsize,color=xlabel_fontcolor)))
    yaxis=dict(visible=True, title=dict(text=ylabel,font=dict(family=ylabel_fontfamily,size=ylabel_fontsize,color=ylabel_fontcolor)))

    fig.update_layout(paper_bgcolor=paper_bgcolor,
    plot_bgcolor=plot_bgcolor,
    xaxis = xaxis,
    yaxis = yaxis)

    fig.update_xaxes(tickangle=float(pa["xticks_rotation"]), tickfont=dict(size=float(pa["xticks_fontsize"])))
    fig.update_yaxes(tickangle=float(pa["yticks_rotation"]), tickfont=dict(size=float(pa["yticks_fontsize"])))

    #UPDATE GRID PROPERTIES
    gridwidth=float(pa["grid_width"])
    if pa["grid_color"]=="None":
        gridcolor=None
    else:
        gridcolor=pa["grid_color"]

    if pa["grid_value"] == "None":
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

    elif pa["grid_value"]=="x":
        fig.update_yaxes(showgrid=True,gridcolor=gridcolor,gridwidth=gridwidth)
    elif pa["grid_value"]=="y":
        fig.update_xaxes(showgrid=True,gridcolor=gridcolor,gridwidth=gridwidth)
    elif pa["grid_value"]=="both":
        fig.update_xaxes(showgrid=True,gridcolor=gridcolor,gridwidth=gridwidth)
        fig.update_yaxes(showgrid=True,gridcolor=gridcolor,gridwidth=gridwidth)

    fig.update_layout(template='plotly_white')

    #UPDATE LEGEND PROPERTIES
    if pab["show_legend"]==True:

        labels=[x["label"] for x in pa["groups_settings"].values()]

        if pa["legend_bgcolor"]=="None":
            legend_bgcolor=None
        else:
            legend_bgcolor=pa["legend_bgcolor"]
        
        if pa["legend_bordercolor"]=="None":
            legend_bordercolor=None
        else:
            legend_bordercolor=pa["legend_bordercolor"]
        
        if pa["legend_borderwidth"]=="":
            legend_borderwidth=0
        else:
            legend_borderwidth=float(pa["legend_borderwidth"])
        
        if pa["legend_fontfamily"]=="Default":
            legend_fontfamily=None
        else:
            legend_fontfamily=pa["legend_fontfamily"]

        if pa["legend_fontcolor"]=="None":
            legend_fontcolor=None
        else:
            legend_fontcolor=pa["legend_fontcolor"]

        legend_fontsize=int(pa["legend_fontsize"])

        legend_title=pa["legend_title"]

        if pa["legend_title_fontfamily"]=="Default":
            legend_title_fontfamily=None
        else:
            legend_title_fontfamily=pa["legend_title_fontfamily"]

        if pa["legend_title_fontcolor"]=="None":
            legend_title_fontcolor=None
        else:
            legend_title_fontcolor=pa["legend_title_fontcolor"]

        legend_title_fontsize=int(pa["legend_title_fontsize"])

        if pa["legend_orientation"]=="vertical":
            legend_orientation="v"
        elif pa["legend_orientation"]=="horizontal":
            legend_orientation="h"

        legend_traceorder=pa["legend_traceorder"]

        if pa["legend_tracegroupgap"]=="":
            legend_tracegroupgap=10
        else:
            legend_tracegroupgap=float(pa["legend_tracegroupgap"])

        if pa["legend_x"]=="":
            legend_x=1.02
        else:
            legend_x=float(pa["legend_x"])
        
        if pa["legend_y"]=="":
            legend_y=1
        else:
            legend_y=float(pa["legend_y"])
        
        legend_valign=pa["legend_valign"]
        legend_title_side=pa["legend_side"]

        
        fig.update_layout(showlegend=True,legend=dict(bgcolor=legend_bgcolor,bordercolor=legend_bordercolor,borderwidth=legend_borderwidth,valign=legend_valign,\
            font=dict(family=legend_fontfamily,size=legend_fontsize,color=legend_fontcolor),orientation=legend_orientation,traceorder=legend_traceorder,tracegroupgap=legend_tracegroupgap,\
            title=dict(text=legend_title,side=legend_title_side,font=dict(family=legend_title_fontfamily,size=legend_title_fontsize,color=legend_title_fontcolor))))
    
    else:
        fig.update_layout(showlegend=False)
    

    return fig

STANDARD_SIZES=[ str(i) for i in list(range(101)) ]
STANDARD_COLORS=["None","aliceblue","antiquewhite","aqua","aquamarine","azure","beige",\
    "bisque","black","blanchedalmond","blue","blueviolet","brown","burlywood",\
    "cadetblue","chartreuse","chocolate","coral","cornflowerblue","cornsilk",\
    "crimson","cyan","darkblue","darkcyan","darkgoldenrod","darkgray","darkgrey",\
    "darkgreen","darkkhaki","darkmagenta","darkolivegreen","darkorange","darkorchid",\
    "darkred","darksalmon","darkseagreen","darkslateblue","darkslategray","darkslategrey",\
    "darkturquoise","darkviolet","deeppink","deepskyblue","dimgray","dimgrey","dodgerblue",\
    "firebrick","floralwhite","forestgreen","fuchsia","gainsboro","ghostwhite","gold",\
    "goldenrod","gray","grey","green","greenyellow","honeydew","hotpink","indianred","indigo",\
    "ivory","khaki","lavender","lavenderblush","lawngreen","lemonchiffon","lightblue","lightcoral",\
    "lightcyan","lightgoldenrodyellow","lightgray","lightgrey","lightgreen","lightpink","lightsalmon",\
    "lightseagreen","lightskyblue","lightslategray","lightslategrey","lightsteelblue","lightyellow",\
    "lime","limegreen","linen","magenta","maroon","mediumaquamarine","mediumblue","mediumorchid",\
    "mediumpurple","mediumseagreen","mediumslateblue","mediumspringgreen","mediumturquoise",\
    "mediumvioletred","midnightblue","mintcream","mistyrose","moccasin","navajowhite","navy",\
    "oldlace","olive","olivedrab","orange","orangered","orchid","palegoldenrod","palegreen",\
    "paleturquoise","palevioletred","papayawhip","peachpuff","peru","pink","plum","powderblue",\
    "purple","red","rosybrown","royalblue","rebeccapurple","saddlebrown","salmon","sandybrown",\
    "seagreen","seashell","sienna","silver","skyblue","slateblue","slategray","slategrey","snow",\
    "springgreen","steelblue","tan","teal","thistle","tomato","turquoise","violet","wheat","white",\
    "whitesmoke","yellow","yellowgreen"]
STANDARD_HISTNORMS=['None', 'percent', 'probability', 'density', 'probability density']
STANDARD_SIZES=[ str(i) for i in list(range(101)) ]
LINE_STYLES=["solid", "dot", "dash", "longdash", "dashdot","longdashdot"]
STANDARD_BARMODES=["stack", "group","overlay","relative"]
STANDARD_ORIENTATIONS=['vertical','horizontal']
STANDARD_ALIGNMENTS=["left","right","auto"]
STANDARD_VERTICAL_ALIGNMENTS=["top", "middle","bottom"]
STANDARD_FONTS=["Arial", "Balto", "Courier New", "Default", "Droid Sans", "Droid Serif", "Droid Sans Mono",\
                "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"]
TICKS_DIRECTIONS=["inside","outside",'']
LEGEND_LOCATIONS=['best','upper right','upper left','lower left','lower right','right','center left','center right','lower center','upper center','center']
MODES=["expand",None]
STANDARD_HOVERINFO=["x", "y", "z", "text", "name","all","none","skip","x+y","x+text","x+name",\
                    "y+text","y+name","text+name","x+y+name","x+y+text","x+text+name","y+text+name"]
STANDARD_HISTFUNC=["count","sum","avg","min","max"]
STANDARD_CUMULATIVE_DIRECTIONS=["increasing","decreasing"]
STANDARD_ERRORBAR_TYPES=["percent","constant","sqrt"]
STANDARD_REFERENCES=["container","paper"]
STANDARD_TITLE_XANCHORS=["auto","left","center","right"]
STANDARD_TITLE_YANCHORS=["top","middle","bottom"]
STANDARD_LEGEND_XANCHORS=["auto","left","center","right"]
STANDARD_LEGEND_YANCHORS=["auto","top","middle","bottom"]
STANDARD_TRACEORDERS=["reversed", "grouped", "reversed+grouped", "normal"]
STANDARD_SIDES=["top","left","top left"]
STANDARD_SPIKEMODES=["toaxis", "across", "marker","toaxis+across","toaxis+marker","across+marker","toaxis+across+marker"]


def figure_defaults():
    """Generates default figure arguments.

    Returns:
        dict: A dictionary of the style { "argument":"value"}
    """
    
    # https://matplotlib.org/3.1.1/api/markers_api.html
    # https://matplotlib.org/2.0.2/api/colors_api.html


    # lists allways need to have thee default value after the list
    # eg.:
    # "title_size":standard_sizes,\
    # "titles":"20"
    # "fig_size_x"="6"
    # "fig_size_y"="6"

def figure_defaults():
    plot_arguments={
        "fig_width":"600",\
        "fig_height":"600",\
        "title":'iHistogram',\
        "title_fontsize":"20",\
        "title_fontfamily":"Default",\
        "title_fontcolor":"None",\
        "titles":"20",\
        "opacity":0.8,\
        "paper_bgcolor":"None",\
        "plot_bgcolor":"None",\
        "hoverinfos":STANDARD_HOVERINFO,\
        "hover_alignments":STANDARD_ALIGNMENTS,\
        "histfuncs":STANDARD_HISTFUNC,\
        "references":STANDARD_REFERENCES,\
        "xref":"container",\
        "yref":"container",\
        "x":"0.5",\
        "y":"0.9",\
        "title_xanchors":STANDARD_TITLE_XANCHORS,\
        "title_yanchors":STANDARD_TITLE_YANCHORS,\
        "title_xanchor":"auto",\
        "title_yanchor":"auto",\
        "linewidth":1.0,\
        "show_legend":"on",\
        "errorbar":".off",\
        "errorbar_value":"10",\
        "errorbar_type":"percent",\
        "errorbar_types":STANDARD_ERRORBAR_TYPES,\
        "errorbar_symmetric":".off",\
        "errorbar_color":"darkgrey",\
        "errorbar_width":"2",\
        "errorbar_thickness":"2",\
        "axis_line_width":1.0,\
        "axis_line_color":"lightgrey",\
        "ticks_line_width":1.0,\
        "ticks_color":"lightgrey",\
        "cols":[],\
        "groups":[],\
        "vals":[],\
        "list_of_groups":[],\
        "groups_settings":dict(),\
        "log_scale":".off",\
        "fonts":STANDARD_FONTS,\
        "cumulative_directions":STANDARD_CUMULATIVE_DIRECTIONS,\
        "colors":STANDARD_COLORS,\
        "histnorms":STANDARD_HISTNORMS,\
        "barmode":"overlay",\
        "barmodes":STANDARD_BARMODES,\
        "histtype_value":"bar",\
        "linestyles":LINE_STYLES,\
        "linestyle_value":"",\
        "orientations":STANDARD_ORIENTATIONS, \
        "fontsizes":STANDARD_SIZES,\
        "xlabel_size":STANDARD_SIZES,\
        "ylabel_size":STANDARD_SIZES,\
        "xlabel":"",\
        "ylabel":"",\
        "label_fontfamily":"Default",\
        "label_fontsize":"15",\
        "label_fontcolor":"None",\
        "xlabels":"14",\
        "ylabels":"14",\
        "left_axis":".on" ,\
        "right_axis":".on",\
        "upper_axis":".on",\
        "lower_axis":".on",\
        "tick_left_axis":".on" ,\
        "tick_right_axis":".off",\
        "tick_upper_axis":".off",\
        "tick_lower_axis":".on",\
        "ticks_direction":TICKS_DIRECTIONS,\
        "ticks_direction_value":TICKS_DIRECTIONS[1],\
        "ticks_length":"6.0",\
        "xticks_fontsize":"14",\
        "yticks_fontsize":"14",\
        "xticks_rotation":"0",\
        "yticks_rotation":"0",\
        "x_lower_limit":"",\
        "y_lower_limit":"",\
        "x_upper_limit":"",\
        "y_upper_limit":"",\
        "maxxticks":"",\
        "maxyticks":"",\
        "spikes":["None","both","x","y"],\
        "spikes_value":"None",\
        "spikes_color":"None",\
        "spikes_thickness":"3.0",\
        "dashes":LINE_STYLES,\
        "spikes_dash":"dash",\
        "spikes_mode":"toaxis",\
        "spikes_modes":STANDARD_SPIKEMODES,\
        "grid":["None","both","x","y"],\
        "grid_value":"None",\
        "grid_width":"1",\
        "grid_color":"lightgrey",\
        "legend_title":"",\
        "legend_bgcolor":"None",\
        "legend_borderwidth":"0",\
        "legend_bordercolor":"None",\
        "legend_borderwidth":"0",\
        "legend_fontfamily":"Default",\
        "legend_fontsize":"12",\
        "legend_fontcolor":"None",\
        "legend_title_fontfamily":"Default",\
        "legend_title_fontsize":"12",\
        "legend_title_fontcolor":"None",\
        "legend_orientation":"vertical",\
        "traceorders":STANDARD_TRACEORDERS,\
        "legend_traceorder":"normal",\
        "legend_tracegroupgap":"10",\
        "legend_y":"1",\
        "legend_x":"1.02",\
        "legend_xanchor":"left",\
        "legend_yanchor":"auto",\
        "legend_xanchors":STANDARD_LEGEND_XANCHORS,\
        "legend_yanchors":STANDARD_LEGEND_YANCHORS,\
        "legend_valign":"middle",\
        "valignments":STANDARD_VERTICAL_ALIGNMENTS,\
        "sides":STANDARD_SIDES,\
        "legend_side":"left",\
        "download_format":["png","pdf","svg"],\
        "downloadf":"pdf",\
        "downloadn":"ihistogram",\
        "session_downloadn":"MySession.ihistogram.plot",\
        "inputsessionfile":"Select file..",\
        "session_argumentsn":"MyArguments.ihistogram.plot",\
        "inputargumentsfile":"Select file.."
    }
    return plot_arguments
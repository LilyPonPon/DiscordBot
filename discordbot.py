import discord
import sqlite3
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

db      = sqlite3.connect('db\scheduleDataS2002.db')
lite    = db.cursor()
client  = discord.Client()
tblname = 'Data_Scedule'



@client.event
async def on_ready():
    global mode
    global talname
    mode = 0




@client.event
async def on_message(message):
    global mode

    List=message.content.split()
    Kind = str(List[0])
    
    #-----botの場合強制終了
    if message.author.bot:
        return

    #-----ModeCountrol
    if Kind == "!start":
        if mode == 0:
            mode = 1
            lite.execute("create table " + tblname + "(target,count,name,argscore)")
            await message.channel.send("今月もクラバト頑張るにゃ～～")
            return
        else:
            await message.channel.send("既にクラバト中だよ...")
            return

    if Kind == "!end":
        if mode == 1:
            mode = 0
            db.close()
            await message.channel.send('今月もクラバトお疲れさまだも')
            return
        else:
            await message.channel.send('まだクラバト期間じゃないぞ')
            return

   #-----SearchControl
    if  "確認" in Kind:
        if Kind == '!週確認' or Kind == '！週確認':
            data1 = str(List[1]) 
            lite.execute( 'select * from ' + tblname + ' where count =' + data1 + ' order by 2,1,3,4')
        if Kind == '!ボス確認' or Kind == '！ボス確認':
            data1 =  '\'' + str(List[1]) + "\'"
            lite.execute( 'select * from ' + tblname + ' where target ='+ data1 + ' order by 2,1,3,4')
        if Kind == '!条件確認' or Kind == '！条件確認':
            data1 =  '\'' + str(List[1]) + "\'"
            data2 = str(List[2]) 
            lite.execute( 'select * from ' + tblname + ' where target ='+ data1 + ' and count =' + data2 +  ' order by 1,2,3,4')
        if Kind == '!確認' or Kind == '！確認':
            lite.execute( 'select * from ' + tblname + ' order by 2,1,3,4')
        #--ConvertPng
        table = lite.fetchall()
        sample_data=table
        df = pd.DataFrame(sample_data,columns=['ボス名','周回数','名前','予想ダメージ(万)'])
        fig, ax = plt.subplots(figsize=(4.8,len(sample_data)*0.5))
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=df.values,
            colLabels=df.columns,
            loc='left',
            bbox=[0,0,1,1])
        plt.savefig('table.png')
        await message.channel.send( "●かくにんしたよ")
        await message.channel.send(file=discord.File("table.png"))
        return

    #-----RsvControl
    if Kind == '!予約' or Kind == '！予約':
        #--ErrorCheck
        if len(List) < 4:
            await message.channel.send('情報が足りないにゃ...ぶたないで...')
            return
        #--Insert
        data1 = '\'' + str(List[1]) + "\',"
        data2 = str(List[2]) + ","
        data3 = '\'' + message.author.name + "\',"
        data4 = str(List[3])
        lite.execute("insert into " + tblname + " values(" + data1 + data2 + data3 + data4 + ");" )
        db.commit()
        if int(data4) > 1000:
            await message.channel.send('★稼ぐにゃっ!!!')
        else:
            await message.channel.send('●予約だにゃーん')
        return
    
    #-----DelControl        
    if Kind == '!削除' or Kind == '！削除':    
        #--ErrorCheck
        if len(List) < 3:
            await message.channel.send('情報が足りないにゃ...ぶたないで...')
            return
        #--Delete
        data1 = '\'' + str(List[1]) + "\'"
        data2 = str(List[2]) + ""
        data3 = '\'' +  message.author.name + "\'"
        lite.execute("delete from " + tblname + " where target=" + data1 + " and count=" + data2 + " and name=" + data3  )
        await message.channel.send('●削除だにゃーん')
        db.commit()
        return
    
    if Kind == '!週削除' or Kind == '！週削除': 
        #--ErrorCheck
        if len(List) < 2:
            await message.channel.send('情報が足りないにゃ...ぶたないで...')
            return
        #--Delete
        data1 = str(List[1])
        lite.execute("delete from " + tblname + " where count=" + data1  )
        await message.channel.send('●削除だにゃーん')
        db.commit()
        return

    if Kind == '!個別削除' or Kind == '！個別削除': 
        #--ErrorCheck
        if len(List) < 3:
            await message.channel.send('情報が足りないにゃ...ぶたないで...')
            return
        #--Delete
        data1 = '\'' + str(List[1]) + "\'"
        data2 = str(List[2]) + ""
        lite.execute("delete from " + tblname + " where target=" + data1 + " and count=" + data2  )
        await message.channel.send('●削除だにゃーん')
        db.commit()
        return
             
    #------Ramdom
    if "やっつん" in message.content and message.author.name=="mazakin":
        await message.channel.send('顔面グラットン')
    if "うんこ" in  message.content:   
        await message.channel.send("( ・∀・)つ うんこー")

# Botの起動とDiscordサーバーへの接続
client.run(os.environ.get('DISCORD_BOT_TOKEN'))

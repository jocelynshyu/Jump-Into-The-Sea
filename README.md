# Jump-Into-The-Sea

原作者：https://github.com/flyxiang1206

仿"赤燭遊戲"混元萬劫活動的 Discord 機器人

為了滿足活動結束後，大家的跳海慾望而生

也為了沒有跳過海但想跳夷下的我

> 警告：有些已知 BUG 還沒修，以及這是我第一次寫 python，code 醜請見諒

## 超簡略 deploy to railway 的流程

1. discord bot
   - 編輯大頭貼
   - bot username
   - copy token for TOKEN
2. discord
   - 邀請 bot 進伺服器
   - 如果還沒開過的話，開啟開發者模式
   - copy channel id for CHANNEL_ID
3. railway
   - deploy from github repo
   - add variables: TOKEN & CHANNEL_ID
4. 可以跳ㄌ

## 結語

### 感謝赤燭遊戲提供這次活動

### ☀️ 以太陽為名，向大道而行 🙏🏻

## 已知錯誤

- Discord 連線會莫名中斷，導致交互失敗，目前不確定原因

  > 暫時認定是 `discord.ui.view` timeout，已嘗試修正持續觀察中

- CSV 檔資料未滿三個元素時程式會錯誤
  > 目前沒考慮修這個

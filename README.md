黑白棋 

(電腦使用Minimax決策自動下棋，玩家挑戰是否能贏電腦)

1. 遊戲概述
棋盤：使用8x8方格棋盤。
棋子：雙面棋子，一面為黑色，一面為白色。初始時，棋盤中央放置兩黑兩白，呈對角排列。
玩家：兩名玩家，分別控制黑色和白色棋子。

2. 遊戲目標
在棋盤上擺放棋子，使得自己的棋子數量在遊戲結束時多於對方。

3. 基本規則
行動輪流：兩名玩家輪流行動，黑棋先行。
每次放置一枚棋子，棋子必須夾住對方的棋子不能孤立地放置。
翻轉棋子：當放置一枚棋子時，所有被夾住的對方棋子都會翻轉成自己的顏色。
無法行動：如果玩家無法進行合法行動，輪到對方行動。若雙方都無法行動，則遊戲結束。
遊戲結束：當棋盤填滿或雙方都無法行動時，遊戲結束。計算棋盤上各自顏色的棋子數量，數量多者獲勝。

#!/usr/bin/env python

import wx
import math

class CSFrame(wx.Frame):
    '''
    A Frame that says Hubner ctm
    '''
    isTransposition = True

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(CSFrame, self).__init__(*args, **kw)
        self.SetMinSize(wx.Size(600, 500))

        # create a panel in the frame
        pnl = wx.Panel(self)

        # put some text with a larger bold font on it
        self.stTitle = wx.StaticText(pnl, label=self.getTitle(), style = wx.ALIGN_CENTRE)
        font = self.stTitle.GetFont()
        font.PointSize += 5
        font = font.Bold()
        self.stTitle.SetFont(font)

        # and create a vboxMain to manage the layout of child widgets
        self.vboxMain = wx.BoxSizer(wx.VERTICAL)
        
        pnl.SetSizer(self.vboxMain)

        # Message horizontal box
        hboxMessage = wx.BoxSizer(wx.HORIZONTAL) 

        hboxMessage.AddSpacer(15)
        stMessage = wx.StaticText(pnl, label='Mensaje', size=(75, -1))
        hboxMessage.Add(stMessage, 0, wx.ALIGN_LEFT|wx.ALL, 5)

        self.tcMessage = wx.TextCtrl(pnl, size=(300, -1))
        hboxMessage.Add(self.tcMessage, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 5)
        hboxMessage.AddSpacer(15)

        # Key horizontal box
        hboxKey = wx.BoxSizer(wx.HORIZONTAL) 

        hboxKey.AddSpacer(15)
        stKey = wx.StaticText(pnl, label='Clave', size=(75, -1))
        hboxKey.Add(stKey, 0, wx.ALIGN_LEFT|wx.ALL, 5)

        self.tcKey = wx.TextCtrl(pnl, size=(300, -1))
        hboxKey.Add(self.tcKey, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 5)
        hboxKey.AddSpacer(15)

        # Buttons horizontal box
        hboxButtons = wx.BoxSizer(wx.HORIZONTAL) 
        # Cifrar button
        btnCifrar = wx.Button(pnl, wx.ID_ANY, 'Cifrar')
        btnCifrar.Bind(wx.EVT_BUTTON, self.encrypt)
        # Descifrar button
        btnDescifrar = wx.Button(pnl, wx.ID_ANY, 'Descifrar')
        btnDescifrar.Bind(wx.EVT_BUTTON, self.decrypt)
        # Add both buttons to hbox
        hboxButtons.Add(btnCifrar, 0, wx.ALL, 5)
        hboxButtons.AddSpacer(10)
        hboxButtons.Add(btnDescifrar, 0, wx.ALL, 5)

        # Results
        self.tcResults = wx.TextCtrl(pnl, style=wx.TE_MULTILINE|wx.TE_READONLY)

        # Change mode
        btnchange = wx.Button(pnl, wx.ID_ANY, 'Alternar')
        btnchange.Bind(wx.EVT_BUTTON, self.alternateMode)
        
        # Add both horizontal boxes
        self.vboxMain.Add(self.stTitle, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 15)
        self.vboxMain.AddSpacer(10)
        self.vboxMain.Add(hboxMessage, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)
        self.vboxMain.Add(hboxKey, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)
        self.vboxMain.AddSpacer(15)
        self.vboxMain.Add(hboxButtons, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.vboxMain.AddSpacer(15)
        self.vboxMain.Add(self.tcResults, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 15)
        self.vboxMain.AddSpacer(15)
        self.vboxMain.Add(btnchange, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.vboxMain.AddSpacer(15)


    def getTitle(self):
        return 'Cifrado por transposición' if self.isTransposition else 'Cifrado del César'

    def alternateMode(self, event):
        self.isTransposition = not self.isTransposition
        self.stTitle.SetLabel(self.getTitle())
        self.vboxMain.Layout()

    def encrypt(self, event):
        self.tcResults.SetValue('')

        # Variables
        preKey = self.tcKey.GetLineText(0)
        message = self.tcMessage.GetLineText(0)

        if not message.strip() or not preKey.strip():
            if not message.strip() and not preKey.strip():
                self.tcResults.WriteText('Error: Los campos MENSAJE y CLAVE se encuentran vacíos.')
                return
            elif not preKey.strip():
                self.tcResults.WriteText('Error: El campo CLAVE se encuentra vacío.')
                return
            else:
                self.tcResults.WriteText('Error: El campo MENSAJE se encuentra vacío.')
                return

        try:
            key = int(preKey)
        except ValueError:
            self.tcResults.WriteText('Error: Asegúrese de ingresar un ENTERO como clave.')
            return

        if self.isTransposition:
            #Cada cadena de texto en el mensaje cifrado representa una columna en la matriz
            ciphertext = [''] * key

            # recorremos las columnas
            for col in range(key):
                pointer = col

                #Lee cada elemento de la columna
                while pointer < len(message):
                    # Pone el caracter que encuentra en el indice de la matriz
                    ciphertext[col] += message[pointer]

                    #mueve el puntero al siguiente elemento de la columna
                    pointer += key

            # Convertimos la lista en una cadena de texto y  lo retornamos
            self.tcResults.WriteText(''.join(ciphertext))
        else:
            self.cesar(True, message, key)

    def decrypt(self, event):
        self.tcResults.SetValue('')

        # Variables
        preKey = self.tcKey.GetLineText(0)
        message = self.tcMessage.GetLineText(0)

        if not message.strip() or not preKey.strip():
            if not message.strip() and not preKey.strip():
                self.tcResults.WriteText('Error: Los campos MENSAJE y CLAVE se encuentran vacíos.')
                return
            elif not preKey.strip():
                self.tcResults.WriteText('Error: El campo CLAVE se encuentra vacío.')
                return
            else:
                self.tcResults.WriteText('Error: El campo MENSAJE se encuentra vacío.')
                return

        try:
            key = int(preKey)
        except ValueError:
            self.tcResults.WriteText('Error: Asegúrese de ingresar un ENTERO como clave.')
            return      

        if self.isTransposition:
            # La función decrypt transposition simula las columnas y filas 
            # de nuestra tabla como el texto plano es escrito usando una lista 
            # de cadenas de texto, primero , necesitamos calcular unos cantos
            # valores

            # El numero de columnas en nuestra tabla
            numOfColumns = math.ceil(len(message) / key)
            # El numero de filas que nuestra tabla necesitara
            numOfRows = key
            # El numero de cajas sombreadas en la ultima columna de nuestra tabla
            numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)

            # Cada cadena de texto in texto plano representa una columna dentro
            # de nuestra tabla
            plaintext = [''] * numOfColumns

            # Las variables col y row señalan el punto en la tabla donde ira el
            # próximo carácter del mensaje enciptado
            col = 0
            row = 0

            for symbol in message:
                plaintext[col] += symbol
                col += 1 # señala la siguiente columna

                # si no hay mas columas  o estamos en un lugar sombreado,volver a 
                # la primera columna y la siguiente fila
                if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
                    col = 0
                    row += 1

            self.tcResults.WriteText(''.join(plaintext))
        else:
            self.cesar(False, message, key)
    
    
    
    # Cesar's algorithm
    def cesar(self, mode, message, key):
        UPPER_LETTERS = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        LOWER_LETTERS = 'abcdefghijklmnñopqrstuvwxyz'
        translated = ''
        
        for symbol in message:
            # Obtenemos el indice del simbolo
            if symbol.isupper():
                num = UPPER_LETTERS.find(symbol) 
                upperFlag = True
            elif symbol.islower():
                num = LOWER_LETTERS.find(symbol) 
                upperFlag = False
            else:
                # Agregamos el simbolo
                translated += symbol
                continue
            
            num = num + key if mode else num - key

            dictLenght = len(UPPER_LETTERS) if upperFlag else len(LOWER_LETTERS)
            # si num es mayor que el largo de
            # LETTERS o es menor que  0
            if num >= dictLenght:
                num = num - dictLenght
            elif num < 0:
                num = num + dictLenght
            
            # Agregamos el simbolo al mensaje final
            translated += UPPER_LETTERS[num] if upperFlag else LOWER_LETTERS[num]
            
        self.tcResults.WriteText(translated)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = CSFrame(None, title='Seguridad informática')
    frm.Centre()
    frm.Show()
    
    app.MainLoop()
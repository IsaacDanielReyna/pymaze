class Vector2:
    def __init__( self, x=0, y=0 ):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    
    def xy( self ):
        return (self.x,self.y)

    def add( self, v2 ):
        result = Vector2()
        result.x = self.x + v2.x
        result.y = self.y + v2.y
        return result

    def sub( self, v2 ):
        result = Vector2()
        result.x = self.x - v2.x
        result.y = self.y - v2.y
        return result

    def scale( self, s ):
        result = Vector2()
        result.x = self.x * s
        result.y = self.y * s
        return result

    def mag( self ):
        return math.sqrt( self.x * self.x + self.y * self.y )
   
    def normalized( self ):
        result = Vector2()
        m = self.mag()
        if m == 0:
            return Vector2( 0, 0 )
        result.x = self.x / m
        result.y = self.y / m
        return result

package main 
 import (
	"net/http"
	"strings"
	"github.com/gin-gonic/gin"
 )

 const (
	ContextKeyUserID = "currentUserID"
	ContextKeyUsername = "currentUsername"
 )

 func Auth() gin.HandlerFunc {
	return func(c *gin.Context){
		authHeader := c.GetHeader("Authorization")
		if authHeader == ""{
			Fail(c, http.StatusUnauthorized, "缺少Token")
			return
		}

		parts := strings.SplitN(authHeader, " ", 2)
		if len(parts) != 2 || !strings.EqualFold(parts[0], "Bearer"){
			Fail(c, http.StatusUnauthorized, "格式无效")
			return
		}

		claims, err := ParseToken(parts[1])
		if err != nil{
			Fail(c, http.StatusUnauthorized, "token无效或过期")
			return
		}

		c.Set(ContextKeyUserID, claims.UserID)
		c.Set(ContextKeyUsername, claims.Username)
		c.next()
	}
 }
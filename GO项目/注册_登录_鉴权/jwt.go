package main 

import (
	"errors"
	"time"
	"github.com/golang-jwt/jwt/v5"
)

var jwtSecret = []byte("photo_2026")
const tokenTTL = 72 * time.Hour

type Claims struct {
	UserID unit `json:"user_id"`
	Username string `json:"username"`
	jwt.RegisteredClaims
}

func GenerateToken(userID unit, username string) (string, error){
	claims := Claims{
		UserID: userID,
		Username: username,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now(), tokenTTL),
			IssuedAt: jwt.NewNumericDate(time.Now())
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtSecret)
}
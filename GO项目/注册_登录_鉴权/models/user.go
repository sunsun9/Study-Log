package models

import (
	"time"
)

type User struct {
	ID unit `grom:"primarykey;autoIncrement" json:"id"`
	Username string `grom:"uniqueIndex;not null" json:"username"`
	Password string `grom:"not null" json:"password"`
	AvatarURL string `json:"avatar_url"`
	CreatedAt time.time `json:"created_at"`
}
from sqlalchemy import Column, Integer, Float, Boolean, String, Date, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from maeum.database.database import Base
import datetime
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid

class MoodWeatherEnum(enum.Enum):
    sunny = "Sunny"
    sunny_cloudy = "SunnyCloudy"
    cloudy = "Cloudy"
    thunder = "Thunder"
    rain = "Rain"

class User(Base):
    __tablename__="user"
    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String, unique=True)
    nickname = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    app_setting = relationship("AppSetting", back_populates="user")


class JournalEntry(Base):
    __tablename__ = "journal_entry"
<<<<<<< Updated upstream
    journal_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id2 = Column(UUID(as_uuid=True))
=======
    journal_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
>>>>>>> Stashed changes
    entry_date = Column(Date)
    context = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)


    mood_temp = relationship("MoodTemperature", back_populates="journal_entry")
    mood_weather = relationship("MoodWeather", back_populates="journal_entry")
    ai_comment = relationship("AIComment", back_populates="journal_entry")
<<<<<<< Updated upstream
    face_expression = relationship("FaceExpression", back_populates="journal_entry")
=======
    journal_risk_hit = relationship("JournalRiskHit", back_populates="journal_entry")
    # MoodWeather 관계 추가
    mood_weather = relationship("MoodWeather", back_populates="journal_entry", uselist=False)
>>>>>>> Stashed changes

class MoodTemperature(Base):
    '''일 별 마음 온도 기록'''
    __tablename__ = "mood_temperature"
<<<<<<< Updated upstream
    temp_id = Column(as_uuid=True, primary_key=True, index=True)
    user_id2 = Column(UUID(as_uuid=True), ForeignKey="journal_entry.user_id2")
=======
    temp_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
>>>>>>> Stashed changes
    entry_date = Column(Date)
    temperature = Column(Float)
    threadhold_breach = Column(Boolean)
    created_at = Column(Date, default=datetime.datetime.now)

<<<<<<< Updated upstream
    journal_entry = relationship("JournalEntry", back_populates="mood_temperature")

class MoodWeatherEnum(enum.Enum):
    sunny = "Sunny"
    sunny_cloudy = "SunnyCloudy"
    cloudy = "Cloudy"
    thunder = "Thunder"
    rain = "Rain"

class MoodWeather(Base):
    '''일기에 대한 날씨(달력에 띄울 것)'''
    __tablename__ = "mood_weather"
    weather_id = Column(UUID(as_uuid=True), primary_key=True)
    weather_code = Column(Enum(MoodWeatherEnum))
    user_id = Column(Integer, ForeignKey("journal_entry.user_id"))
    journal_id = Column(Integer, ForeignKey("journal_entry.journal_id"))
    created_at = Column(DateTime, default=datetime.datetime.now)

    journal_entry = relationship("JournalEntry", back_populates="mood_weather", uselist=False)


class AIComment(Base):
    '''일기에 출력할 ai의 코멘트'''
    _tablename__ = "ai_comment"
    comment_id = Column(Integer, primary_key=True, index=True)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    model_version = Column(String)
    journal_id = Column(UUID(as_uuid=True), ForeignKey="journal_entry.journal_id")

# class FaceEmotionEnum(enum.Enum):
class FaceExpression(Base):
    '''사진 감정 분석 결과'''
    __tablename__ = "face_expression"
    expr_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    label = ()
    confidence = Column(Float)
    model_version = Column(String)
    capture_at = Column(Date)
    journal_id = Column(UUID(as_uuid=True), ForeignKey="journal_entry.journal_id")

    journal_entry = relationship("JournalEntry", back_populates="face_expression")
=======
    user = relationship("User", back_populates="mood_temperature")

# MoodWeather 테이블 정의: 일기에 대한 날씨(달력에 띄울 것)
class MoodWeather(Base):
    __tablename__ = "mood_weather"
    weather_id = Column(UUID(as_uuid=True), primary_key=True)
    weather_code = Column(Enum(MoodWeatherEnum))
    journal_id = Column(UUID(as_uuid=True), ForeignKey("journal_entry.journal_id"))
    created_at = Column(DateTime, default=datetime.datetime.now)

    journal_entry = relationship("JournalEntry", back_populates="mood_weather", uselist=False)

class AIComment(Base):
    '''일기에 출력할 ai의 코멘트'''
    __tablename__ = "ai_comment"
    comment_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    journal_id = Column(UUID(as_uuid=True), ForeignKey("journal_entry.journal_id"))

    journal_entry = relationship("JournalEntry", back_populates="ai_comment")

class JournalRiskHit(Base):
    __tablename__ = "journal_risk_hit"
    hit_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    risk_id = Column(UUID(as_uuid=True), ForeignKey("risk_keyword.risk_id"))
    matched_text = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    journal_id = Column(UUID(as_uuid=True), ForeignKey("journal_entry.journal_id"))

    journal_entry = relationship("JournalEntry", back_populates="journal_risk_hit")
    risk_keyword = relationship("RiskKeyword", back_populates="journal_risk_hit")

class RiskKeyword(Base):
    __tablename__ = "risk_keyword"
    risk_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    keyword = Column(String)
    active = Column(Boolean)

    journal_risk_hit = relationship("JournalRiskHit", back_populates="risk_keyword")
    
class FaceExpressionEnum(enum.Enum):
    happy = "Happy"
    sad = "Sad"
    neutral = "Neutral"
    angry = "Angry"
    fear = "Fear"
    surprise = "Surprise"
    disgust = "Disgust"

# class FaceEmotionEnum(enum.Enum):
class FaceExpression(Base):
    '''사진 감정 분석 결과'''
    __tablename__ = "face_expression"
    expr_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    label = Column(Enum(FaceExpressionEnum))
    confidence = Column(Float)
    model_version = Column(String)
    captured_at = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))

    user = relationship("User", back_populates="face_expression")

>>>>>>> Stashed changes

class JournalAnalysis(Base):
    __tablename__ = "journal_analysis"
    analysis_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    date = Column(Date)
    happy = Column(Integer)
    soso = Column(Integer)
    anxiety = Column(Integer)
    anger = Column(Integer)
    sadness = Column(Integer)
    journal_id = Column(UUID(as_uuid=True), ForeignKey("journal_entry.journal_id"))

    journal_entry = relationship("JournalEntry", back_populates="journal_analysis")

class AppSetting(Base):
    __tablename__ = "app_setting"
    setting_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
<<<<<<< Updated upstream
    user_id2 = Column(UUID(as_uuid=True), ForeignKey="user.user_id")
=======
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
>>>>>>> Stashed changes
    notification_opt_in = Column(Boolean)
    updated_at = Column(Date)

    user = relationship("User", back_populates="app_setting")

class HelpAgency(Base):
    agency_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String)
    region = Column(String)
    phone = Column(String)
    url = Column(String)

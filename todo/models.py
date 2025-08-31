from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Profile(models.Model):
    """Extended user profile with additional information"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_picture = models.ImageField(
        upload_to='profile/', 
        blank=True, 
        null=True, 
        default='profile/profile.png',
        help_text="Upload a profile picture"
    )
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Tell us about yourself"
    )
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Contact phone number"
    )
    date_of_birth = models.DateField(
        blank=True, 
        null=True,
        help_text="Your date of birth"
    )
    location = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="City, Country"
    )
    website = models.URLField(
        blank=True, 
        null=True,
        help_text="Personal or professional website"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_name(self):
        """Return user's full name or username if names not available"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username


class TaskCategory(models.Model):
    """Categories for organizing tasks"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Optional description for this category"
    )
    color = models.CharField(
        max_length=7, 
        default='#007bff',
        help_text="Hex color code for category display"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Task Category"
        verbose_name_plural = "Task Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    """Enhanced task model with professional features"""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Required fields
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3)],
        help_text="Brief, descriptive task title"
    )
    
    # Optional fields with null=True and blank=True
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Detailed description of the task"
    )
    category = models.ForeignKey(
        TaskCategory, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='tasks',
        help_text="Task category for organization"
    )
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        help_text="Task priority level"
    )
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text="Current task status"
    )
    due_date = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="When this task should be completed"
    )
    estimated_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Estimated time to complete (in hours)"
    )
    tags = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Comma-separated tags for easy searching"
    )
    notes = models.TextField(
        blank=True, 
        null=True,
        help_text="Additional notes or comments"
    )
    attachment = models.FileField(
        upload_to='task_attachments/', 
        blank=True, 
        null=True,
        help_text="Optional file attachment"
    )
    
    # Tracking fields
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="When the task was marked as completed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'due_date']),
            models.Index(fields=['user', 'priority']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        """Override save to automatically set completed_at timestamp"""
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
        
        # Auto-update status based on completed field
        if self.completed and self.status != 'completed':
            self.status = 'completed'
        elif not self.completed and self.status == 'completed':
            self.status = 'pending'
            
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False

    @property
    def days_until_due(self):
        """Calculate days until due date"""
        if self.due_date and not self.completed:
            delta = self.due_date.date() - timezone.now().date()
            return delta.days
        return None

    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []


class TaskComment(models.Model):
    """Comments and updates on tasks"""
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='task_comments'
    )
    comment = models.TextField(
        help_text="Add a comment or update about this task"
    )
    attachment = models.FileField(
        upload_to='comment_attachments/', 
        blank=True, 
        null=True,
        help_text="Optional file attachment for this comment"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Task Comment"
        verbose_name_plural = "Task Comments"
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment on {self.task.title} by {self.user.username}"


class TaskReminder(models.Model):
    """Reminders for tasks"""
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE,
        related_name='reminders'
    )
    remind_at = models.DateTimeField(
        help_text="When to send the reminder"
    )
    message = models.TextField(
        blank=True, 
        null=True,
        help_text="Custom reminder message"
    )
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Task Reminder"
        verbose_name_plural = "Task Reminders"
        ordering = ['remind_at']

    def __str__(self):
        return f"Reminder for {self.task.title} at {self.remind_at}"